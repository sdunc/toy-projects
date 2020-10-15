# Stephen Duncanson & Alice Hu
# Fall 2019

import random
import math
import numpy as np
import constant as c
from numpy import linalg as LA
from scipy.spatial import cKDTree


class Simulation:
    def __init__(self, n_particles):
        self.n_particles = n_particles
        self.n_accepted_moves = 0
        self.n_rejected_moves = 0
        self.initial_system = generate_original_system(n_particles)
        self.initial_system_energy = calculate_energy(self.initial_system)
        self.initial_system_order_parameter = get_order_parameter(self.initial_system)
        self.current_system_energy = self.initial_system_energy    # originally
        self.current_order_parameter = self.initial_system_order_parameter  # originally
        self.system = self.initial_system   # originally
        self.trial_system = None    # originally
        self.trial_system_energy = None
        self.shifted_particle = None    # originally
        self.original_particle = None   # originally
        setup_vtf_output(n_particles*2)

    def get_initial_order_parameter(self):
        return self.initial_system_order_parameter

    def get_current_energy(self):
        return self.current_system_energy

    def get_acceptance_ratio(self):
        return self.n_accepted_moves / (self.n_rejected_moves + self.n_accepted_moves)

    def get_n_accepted_moves(self):
        return self.n_accepted_moves

    def get_total_delta_energy(self):
        return self.current_system_energy - self.initial_system_energy

    def get_delta_energy(self):
        return self.trial_system_energy - self.current_system_energy


    def generate_trial_move(self):
        trial_results = generate_trial_move(self.system)
        self.trial_system = trial_results[0]
        self.shifted_particle = trial_results[1]
        self.original_particle = trial_results[2]
        self.trial_system_energy = calculate_energy(self.trial_system)

    def accept_trial_move(self):
        self.system = self.trial_system
        self.current_system_energy = self.trial_system_energy
        self.current_order_parameter = get_order_parameter(self.system)
        write_position(self.system)

        write_energy((self.n_rejected_moves + self.n_accepted_moves), self.current_system_energy, self.current_order_parameter, get_bond_ratio(self.system))
        self.n_accepted_moves += 1
        #for n in self.system:
        #    n.break_bond()


    def reject_trial_move(self):
        self.system.remove(self.shifted_particle)
        self.system.append(self.original_particle)
        self.n_rejected_moves += 1
        write_energy((self.n_rejected_moves + self.n_accepted_moves), self.current_system_energy, self.current_order_parameter, get_bond_ratio(self.system))
        #for n in self.system:
        #    n.break_bond()


class Spherocylinder:
    def __init__(self, p1, p2):
        self.p1_position = p1
        self.p2_position = p2
        self.s = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])  # line segment
        self.center_position = np.array([(p2[0] + p1[0]) / 2, (p2[1] + p1[1]) / 2, (p2[2] + p1[2]) / 2])
        self.theta = get_theta(self.s)
        self.phi = get_phi(self.s)
        self.n = np.array([(p2[0] - p1[0]) / 2, (p2[1] - p1[1]) / 2, (p2[2] - p1[2]) / 2])
        self.dipole_moment = 2 * c.Q * self.n
        self.bond_exp = None
        self.bond_angle = None
        self.bonded = False

    def get_bond_exp(self):
        return self.bond_exp

    def get_bond_angle(self):
        return self.bond_angle

    def set_bond_angle(self, bond_angle):
        self.bond_angle = bond_angle

    def set_bond_exp(self, bond_exp):
        self.bond_exp = bond_exp

    #def break_bond(self):
        #self.bonded = False

    def is_bonded(self):
        return self.bonded

    def bond(self):
        self.bonded = True

    def get_dipole_moment(self):
        return self.dipole_moment

    def get_center_position(self):
        return self.center_position

    def get_p1_position(self):
        return self.p1_position

    def get_p2_position(self):
        return self.p2_position

    def get_s(self):
        return self.s

    def get_n(self):
        return self.n

    def get_theta(self):
        return self.theta

    def get_phi(self):
        return self.phi

    def set_theta(self, new_theta):
        self.theta = new_theta

    def set_phi(self, new_phi):
        self.phi = new_phi


def get_phi(s):
    phi = math.acos(s[2] / c.S_LENGTH)  # arc-cosine(z_component/magnitude of S)
    return phi


def get_theta(s):
    phi = get_phi(s)
    rho = c.S_LENGTH * math.sin(phi)  # combine both get_theta & phi
    ratio = s[0] / rho
    if ratio > 1:
        ratio = 1
    elif ratio < -1:
        ratio = -1
    theta = math.acos(ratio)
    return theta


def unit_vector(s):
    return s / LA.norm(s)


def get_magnitude(s):
    return LA.norm(s)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    degree = (180*np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))/c.PI  # returns angle in degrees
    return degree


def create_segment(p1, p2):
    s = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    return s


def get_random_p1():
    x = random.uniform(0, c.X_BOUND)
    y = random.uniform(0, c.Y_BOUND)
    z = random.uniform(0, c.Z_BOUND)
    p1 = np.array([x, y, z])
    return p1


def get_random_p2(p1):
    theta = random.uniform(0, 360)
    phi = random.uniform(-90, 90)
    rho = c.S_LENGTH * math.sin(phi)

    x2 = p1[0] + rho * math.cos(theta)
    y2 = p1[1] + rho * math.sin(theta)
    z2 = p1[2] + c.S_LENGTH * math.cos(phi)
    p2 = np.array([x2, y2, z2])
    return p2


def check_intersection(particle1, particle2):
    small_num = 0.0000001  # number to check if they're closely parallel
    u = particle1.get_s()  # s1
    v = particle2.get_s()  # s2
    p0 = particle1.get_p1_position()  # P0
    q0 = particle2.get_p1_position()  # Q0
    w = np.array([p0[0] - q0[0], p0[1] - q0[1], p0[2] - q0[2]])  # distance from 2 particles from their p1's

    a = np.dot(u, u)
    b = np.dot(u, v)
    f = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)
    D = (a * f) - (b * b)  # always >=0

    # Set all to defaults
    sc = D
    sN = D
    sD = D  # sc = sN / sD, default sD = D >= 0
    tc = D
    tN = D
    tD = D  # tc = tN / tD, default tD = D >= 0

    if D * D < small_num:  # checks if SCs are parallel
        sN = 0.0  # force using point P0 on segment S1
        sD = 1.0  # to prevent possible division by 0.0 later
        tN = e
        tD = f
    else:  # get the closest points on the infinite lines
        sN = (b * e) - (f * d)
        tN = (a * e) - (b * d)
        if sN < 0.0:
            sN = 0.0
            tN = e
            tD = f
        elif sN > sD:  # sc > 1  => the s=1 edge is visible
            sN = sD
            tN = (e + b)
            tD = f
    if tN < 0.0:  # tc < 0 => the t=0 edge is visible
        tN = 0.0
        # recompute sc for this edge
        if -d < 0.0:
            sN = 0.0
        elif -d > a:
            sN = sD
        else:
            sN = -d
            sD = a
    elif tN > tD:  # tc > 1  => the t=1 edge is visible
        tN = tD
        # recompute sc for this edge
        if (-d + b) < 0.0:
            sN = 0.0
        elif (-d + b) > a:
            sN = sD
        else:
            sN = (-d + b)
            sD = a
    # division to get sc and tc
    if abs(sN) < small_num:
        sc = 0.0
    else:
        sc = sN / sD
    if abs(tN) < small_num:
        tc = 0.0
    else:
        tc = tN / tD
    # difference of 2 closest points
    dP = np.array(
        [w[0] + (sc * u[0]) - (tc * v[0]), w[1] + (sc * u[1]) - (tc * v[1]), w[2] + (sc * u[2]) - (tc * v[2])])
    # dP = w + np.multiply(sc,u) - np.multiply(tc,v) # #S1(sc) - S2(tc)
    close_d = dP[0] * dP[0] + dP[1] * dP[1] + dP[2] * dP[2]  # closest distance b/w 2 lines
    # check if distance <= radius * 2, if so, INTERSECTION!
    if close_d <= (2 * (c.RADIUS + c.S_RADIUS)) * (
            2 * (c.RADIUS + c.S_RADIUS)):  # used squared distance of twice the radius as cutoff
        return True
    else:
        return False


def there_are_intersections(close_list, particle_list):
    if len(close_list) > 1:  # If there are more than 1 close neighbors (including the  particle itself)
        particle1 = particle_list[-1]  # ????                 #Since the shifted or added particle was just added it should be the last in the list
        close_list.remove(particle_list.index(particle1))  # Remove the particle itself from the list of close particles
        for p in close_list:  # for every other close particle
            particle2 = particle_list[p]  # The second particle is the that index inside the particle list
            if check_intersection(particle1, particle2):
                return True  # if the check_intersecton function returns true (collision!) then it returns false (there ARE collisions)
        return False  # if there are no intersections, return true
    else:  # If the length of the list of close partcles is <= 1, there are no close neighbors
        return False  # Therefore there are no collisions, return true and save computation


def generate_original_system(n):
    particle_list = []
    while len(particle_list) < n:
        p1 = get_random_p1()
        p2 = get_random_p2(p1)
        new_p = Spherocylinder(p1, p2)
        particle_list.append(new_p)
        ens = create_pbc(particle_list)
        pbc_list = ens + particle_list
        kdtree = cKDTree([x.get_center_position() for x in pbc_list])
        close_list = list(kdtree.query_ball_point(new_p.get_center_position(), c.COLLISON_DISTANCE))

        if there_are_intersections(close_list, pbc_list):
            particle_list.remove(new_p)
    return particle_list


def generate_trial_move(PARTICLE_LIST):
    old_particle = PARTICLE_LIST.pop(random.randint(0, len(PARTICLE_LIST) - 1))

    while True:
        translation_or_rotation = random.randint(0, 1)
        if translation_or_rotation == 0:
            shifted_particle = get_rotated_p(old_particle)
        elif translation_or_rotation == 1:
            shifted_particle = get_moved_p(old_particle)

        PARTICLE_LIST.append(shifted_particle)
        pbc_list = create_pbc(PARTICLE_LIST) + PARTICLE_LIST
        trial_kdtree = cKDTree([x.get_center_position() for x in pbc_list])
        trial_close_list = list(trial_kdtree.query_ball_point(shifted_particle.get_center_position(), c.COLLISON_DISTANCE))
        if not there_are_intersections(trial_close_list, pbc_list):
            return PARTICLE_LIST, shifted_particle, old_particle
        else:
            PARTICLE_LIST.remove(shifted_particle)


def create_pbc(PARTICLE_LIST):
    ens = []
    for x in PARTICLE_LIST:
        m = x.get_center_position()
        if m[0] < c.PBC_X_LEFT_BOUND:
            p1 = x.get_p1_position()
            p2 = x.get_p2_position()
            new_p1 = np.array([p1[0] + c.X_BOUND, p1[1], p1[2]])
            new_p2 = np.array([p2[0] + c.X_BOUND, p2[1], p2[2]])
            s = Spherocylinder(new_p1, new_p2)
            ens.append(s)
        elif m[0] > c.PBC_X_RIGHT_BOUND:
            p1 = x.get_p1_position()
            p2 = x.get_p2_position()
            new_p1 = np.array([p1[0] - c.X_BOUND, p1[1], p1[2]])
            new_p2 = np.array([p2[0] - c.X_BOUND, p2[1], p2[2]])
            s = Spherocylinder(new_p1, new_p2)
            ens.append(s)
        elif m[1] < c.PBC_Y_LEFT_BOUND:
            p1 = x.get_p1_position()
            p2 = x.get_p2_position()
            new_p1 = np.array([p1[0], p1[1] + c.Y_BOUND, p1[2]])
            new_p2 = np.array([p2[0], p2[1] + c.Y_BOUND, p2[2]])
            s = Spherocylinder(new_p1, new_p2)
            ens.append(s)
        elif m[1] > c.Y_BOUND - (c.S_LENGTH / 2 + c.S_RADIUS):
            p1 = x.get_p1_position()
            p2 = x.get_p2_position()
            new_p1 = np.array([p1[0], p1[1] - c.Y_BOUND, p1[2]])
            new_p2 = np.array([p2[0], p2[1] - c.Y_BOUND, p2[2]])
            s = Spherocylinder(new_p1, new_p2)
            ens.append(s)
        elif m[2] < c.PBC_Z_LEFT_BOUND:
            p1 = x.get_p1_position()
            p2 = x.get_p2_position()
            new_p1 = np.array([p1[0], p1[1], p1[2] + c.Z_BOUND])
            new_p2 = np.array([p2[0], p2[1], p2[2] + c.Z_BOUND])
            s = Spherocylinder(new_p1, new_p2)
            ens.append(s)
        elif m[2] > c.Z_BOUND - (c.S_LENGTH / 2 + c.S_RADIUS):
            p1 = x.get_p1_position()
            p2 = x.get_p2_position()
            new_p1 = np.array([p1[0], p1[1], p1[2] - c.Z_BOUND])
            new_p2 = np.array([p2[0], p2[1], p2[2] - c.Z_BOUND])
            s = Spherocylinder(new_p1, new_p2)
            ens.append(s)
    return ens


def calculate_energy(particle_list):
    total_energy = 0
    pbc_list = create_pbc(particle_list)
    p2_kdtree = cKDTree([x.get_p2_position() for x in particle_list])
    p2_pbc_tree = cKDTree([x.get_p2_position() for x in pbc_list])

    for particle1 in particle_list:
        c_t = 1
        particle1_p1 = particle1.get_p1_position()
        particle1_p2 = particle1.get_p2_position()
        close_p2s = list(p2_kdtree.query_ball_point(particle1.get_p1_position(), c.IC))
        pbc_close_p2s = list(p2_pbc_tree.query_ball_point(particle1.get_p1_position(), c.IC))
        close_p2s = pbc_close_p2s + close_p2s
        for p2 in close_p2s:
            particle2 = particle_list[p2]
            particle2_p2 = particle2.get_p2_position()
            a = create_segment(particle1_p2, particle1_p1)  # normal vector
            b = create_segment(particle1_p2, particle2_p2)  # vector b/w 2 SCs
            theta = angle_between(a, b)
            particle2.set_bond_angle(theta)
            g = math.exp(c.EPSILON - (c.K * (1 - math.cos(theta))))
            c_t += g
            particle2.set_bond_exp(g)
        c1 = 1 / c_t  # normalization const.
        for p2 in close_p2s:
            particle2 = particle_list[p2]
            b = particle2.get_bond_exp()
            r = random.uniform(0, 1)
            if r <= b * c1 and not particle2.is_bonded():
                theta = particle2.get_bond_angle()
                total_energy += c.EPSILON - c.K * (1 - math.cos(theta))
                particle2.bond()
                break
    total_energy += calculate_e_field_energy(particle_list)
    return total_energy


def r_get_p1_bond(n, PARTICLE_LIST, cluster):
    particle1 = PARTICLE_LIST[n]
    pbc_list = create_pbc(PARTICLE_LIST) #list of particles interacting periodically
    p2_kdtree = cKDTree([x.get_p2_position() for x in PARTICLE_LIST])
    p2_pbc_tree = cKDTree([x.get_p2_position() for x in pbc_list])
    pbc_close_p2s = list(p2_pbc_tree.query_ball_point(particle1.get_p2_position(), c.IC))
    close_p2s = list(p2_kdtree.query_ball_point(particle1.get_p2_position(), c.IC))
    close_p2s = pbc_close_p2s + close_p2s
    for x in cluster:
        try:
            close_p2s.remove(x)
        except:
            ValueError
    if len(close_p2s) > 0:
        p2 = random.choice(close_p2s)
        cluster.append(p2)
        return r_get_p1_bond(p2, PARTICLE_LIST, cluster)
    else:
        return cluster


def r_get_p2_bond(n, PARTICLE_LIST, cluster):
    particle1 = PARTICLE_LIST[n]
    pbc_list = create_pbc(PARTICLE_LIST)
    p1_kdtree = cKDTree([x.get_p1_position() for x in PARTICLE_LIST])
    p1_pbc_tree = cKDTree([x.get_p1_position() for x in pbc_list])
    pbc_close_p1s = list(p1_pbc_tree.query_ball_point(particle1.get_p1_position(), c.IC))
    close_p1s = list(p1_kdtree.query_ball_point(particle1.get_p1_position(), c.IC))
    close_p1s = pbc_close_p1s + close_p1s
    for x in cluster:
        try:
            close_p1s.remove(x)
        except:
            ValueError
    if len(close_p1s) > 0:
        p1 = random.choice(close_p1s)
        cluster.append(p1)
        return r_get_p1_bond(p1, PARTICLE_LIST, cluster)
    else:
        return cluster


def get_order_parameter(PARTICLE_LIST):
    N = 0
    sum = 0
    norm = c.S_LENGTH/2  # normalize vector
    for i in range(len(PARTICLE_LIST)):
        for j in range(i + 1, len(PARTICLE_LIST)):
            norm2 = np.dot(PARTICLE_LIST[i].get_n()/norm, PARTICLE_LIST[j].get_n()/norm)
            sum += (3 * norm2 * norm2 - 1) / 2
            N += 1
    return sum / N


def calculate_e_field_energy(PARTICLE_LIST):
    total_e_field_energy = 0
    for p in PARTICLE_LIST:
        dipole_moment = p.get_dipole_moment()
        total_e_field_energy += c.E_COEFF * c.E_FIELD_VECTOR * dipole_moment
    return float(total_e_field_energy[2])  # only works in z-direction


def get_rotated_p(p): #rotating about CM
    theta = p.get_theta()
    phi = p.get_phi()
    center = p.get_center_position()

    new_phi = phi + random.uniform(-c.DELTA, c.DELTA)

    px1 = center[0] - (c.S_LENGTH/2 * math.sin(new_phi) * math.cos(theta))
    py1 = center[1] - (c.S_LENGTH/2 * math.sin(new_phi) * math.sin(theta))
    pz1 = center[2] - (c.S_LENGTH/2 * math.cos(new_phi))
    p1 = np.array([px1, py1, pz1])

    px2 = center[0] + (c.S_LENGTH/2 * math.sin(new_phi) * math.cos(theta))
    py2 = center[1] + (c.S_LENGTH/2 * math.sin(new_phi) * math.sin(theta))
    pz2 = center[2] + (c.S_LENGTH/2 * math.cos(new_phi))
    p2 = np.array([px2, py2, pz2])

    new_p = Spherocylinder(p1, p2)
    return new_p


def get_moved_p(p):
    p1 = get_random_p1()
    p2 = get_random_p2(p1)
    NEW_PARTICLE = Spherocylinder(p1, p2)
    return NEW_PARTICLE


def get_volume_fraction():
    total_volume = c.X_BOUND * c.Y_BOUND * c.Z_BOUND
    occupied_volume = c.NUMBER_OF_PARTICLES * (
                c.PI * c.S_RADIUS * c.S_RADIUS * c.S_LENGTH + (4 / 3) * c.PI * c.S_RADIUS * c.S_RADIUS * c.S_RADIUS)
    return occupied_volume / total_volume


def get_bond_ratio(PARTICLE_LIST):
    return len([x for x in PARTICLE_LIST if x.is_bonded()])/len(PARTICLE_LIST)


def setup_vtf_output(num_of_atoms):
    vtf_output_file = open('output.vtf', 'w')
    for i in range(num_of_atoms):
        if i % 2 == 0:
            vtf_output_file.write('atom ' + str(i) + ' radius ' + str(c.RADIUS) + " name S1\n")
        else:
            vtf_output_file.write('atom ' + str(i) + ' radius ' + str(c.RADIUS) + " name S2\n")
    for i in range(int(num_of_atoms/2)):
        first_point = i+i
        second_point = i+(i+1)
        vtf_output_file.write('bond ' + str(first_point) + ':' + str(second_point) + '\n')
    vtf_output_file.close()


def write_position(p):
    vtf_output_file = open('output.vtf', 'a')
    vtf_output_file.write('timestep\n')
    vtf_output_file.write('PBC ' + str(c.X_BOUND) + ' ' + str(c.Y_BOUND) + ' ' + str(c.Z_BOUND) + '\n')
    for o in p: #for every particle in the system
        p1_pos = o.get_p1_position()
        p2_pos = o.get_p2_position()
        vtf_output_file.write(str(float(p1_pos[0])) + ' ' + str(float(p1_pos[1])) + ' ' + str(float(p1_pos[2])) + '\n')
        vtf_output_file.write(str(float(p2_pos[0])) + ' ' + str(float(p2_pos[1])) + ' ' + str(float(p2_pos[2])) + '\n')
    vtf_output_file.close()


def write_energy(count, energy, order_parameter, bond_ratio):
    energy_output_file = open('energy.txt', 'a')
    energy_output_file.write(str(count) + ',' + str(energy) + ',' + str(order_parameter) + ',' + str(bond_ratio) + '\n')
    energy_output_file.close()
