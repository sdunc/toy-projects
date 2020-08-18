# Constant Fraction Discriminator

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift
from scipy.signal import find_peaks


def pileup_adjust(edges, width=4, delta_width=2):
    # an idea to %mod wide peaks by 4 and count possible stacks
    # may not be needed if I can get parameters right
    widths = edges[1::2] - edges[:-1:2]
    print(widths)
    stacked_bool = widths > width + delta_width
    #np.append(rising_edge, new_edges)
    print(stacked_bool)
    rising_edge = edges[::2]
    return rising_edge


def cfd(signal, fraction, delay=1, threshold=20):
    """Constant Fraction Discriminator
    :param np.array signal: the input from the digitizer
    :param float fraction: the fraction, from 0 to 1
    :param float delay: the delay of the CFD
    :param float threshold: the threshold
    :return np.array edge_indices: the start and stop indices for each peak
    """

    # Scaled and delayed signal
    scaled = signal * fraction
    delayed = shift(scaled, -delay, mode="nearest")
    
    cfd_signal = signal - delayed
    plt.xlim(0, len(spectrum))
    plt.ylim(0, max(spectrum)+20)
    plt.plot(signal, '--', alpha=.5, color='blue', label='original signal')
    plt.plot(scaled, ':', alpha=.5, color='red', label='scaled signal')
    plt.plot(delayed,'-.', alpha=.5, color='green', label='delayed signal')
    plt.plot(cfd_signal,'-', color='black',label='cfd_signal')
    plt.axhline(threshold, linestyle='-', color='black', alpha=.3, label='threshold')
    plt.title("CFD processing (Ar 2+ Data)")
    plt.xlabel("tof (.5ns)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()
    # Edge detection
    # edges_bool is true when signal is above threshold
    edges_bool = cfd_signal > threshold

    # edges bool 2
    # XOR comparison of edges_bool[1:], edges_bool[:-1]
    # Returns true if odd number of trues
    # compares each element of edges_bool with neighbor
    # if one is false and one is true
    # returns true
    # meaning that one index is below threshold
    # one is above
    # this is an edge of the peak
    edges_bool_2 = np.logical_xor(edges_bool[1:],edges_bool[:-1])
    
    # Edge indicies are where edges_bool_2 is true
    # np.squeeze() just makes it 1d
    edge_index = np.squeeze(np.where(edges_bool_2 == True))
    print(edge_index)
    
    return edge_index
        

if __name__ == "__main__":

    #Ar2+ Data
  #  spectrum = np.array([-2.1741943, -2.1741943, -0.17419434, 1.8258057, -1.1741943, -4.1741943, 1.8258057, 4.8258057, 40.825806, 125.825806, 208.8258, 207.8258, 130.8258, 35.825806, -17.174194, -46.174194, -48.174194, -32.174194, -17.174194, -2.1741943, -4.1741943, -8.174194, -1.1741943, -6.1741943, -5.1741943, -5.1741943, -6.1741943, 4.8258057, 31.825806, 120.825806, 248.8258, 298.8258, 233.8258, 149.8258, 159.8258, 254.8258, 310.8258, 262.8258, 148.8258, 92.825806, 131.8258, 192.8258, 233.8258, 290.8258, 414.8258, 556.8258, 565.8258, 411.8258, 187.8258, 10.825806, -84.174194, -90.174194, -79.174194, -32.174194, 63.825806, 238.8258, 413.8258, 449.8258, 326.8258, 153.8258, 15.825806, -52.174194, -60.174194, -33.174194, 25.825806, 126.825806, 206.8258, 220.8258, 244.8258, 392.8258, 586.8258, 695.8258, 654.8258, 476.8258, 235.8258, 55.825806, -36.174194, -60.174194, -41.174194, -17.174194])
    #Ar3+ Data
    #spectrum = np.array([-2.1741943, 3.8258057, 9.825806, 67.825806, 206.8258, 438.8258, 678.8258, 790.8258, 690.8258, 435.8258, 163.8258, -30.174194, -90.174194, -90.174194, -64.174194, 105.825806, 488.8258, 997.8258, 1300.8258, 1304.8258, 1093.8258, 756.8258, 358.8258, 93.825806, 89.825806, 357.8258, 695.8258, 896.8258, 863.8258, 663.8258, 503.8258, 540.8258, 674.8258, 674.8258, 489.8258, 238.8258, 38.825806, 8.825806, 132.8258, 277.8258, 310.8258, 225.8258, 108.825806, 13.825806, -22.174194, -11.174194, 4.8258057, 27.825806, 41.825806, 47.825806, 59.825806, 151.8258, 336.8258, 575.8258, 756.8258, 765.8258, 568.8258, 281.8258, 45.825806, -76.174194, -90.174194, -60.174194, -14.174194, 21.825806, 40.825806, 31.825806, 12.825806, 7.8258057, -1.1741943, 4.8258057, 29.825806, 129.8258, 282.8258, 367.8258, 307.8258, 176.8258, 52.825806, -26.174194, -52.174194, -32.174194])
    #Ar4+ Data
    #spectrum = np.array([-0.17419434, 6.8258057, 46.825806, 140.8258, 232.8258, 225.8258, 153.8258, 117.825806, 225.8258, 396.8258, 493.8258, 487.8258, 440.8258, 349.8258, 205.8258, 51.825806, -19.174194, 36.825806, 183.8258, 273.8258, 253.8258, 148.8258, 40.825806, -31.174194, -53.174194, -47.174194, -19.174194, 3.8258057, 7.8258057, 12.825806, 9.825806, 10.825806, 7.8258057, 8.825806, 13.825806, 10.825806, 12.825806, 13.825806, 16.825806, 18.825806])
    #Ar5+ Data
    spectrum = np.array([0.82580566, -3.1741943, 0.82580566, -1.1741943, -2.1741943, -2.1741943, 2.8258057, -2.1741943, 24.825806, 109.825806, 234.8258, 270.8258, 207.8258, 107.825806, 108.825806, 211.8258, 309.8258, 316.8258, 335.8258, 436.8258, 531.8258, 476.8258, 301.8258, 105.825806, -20.174194, -29.174194, 123.825806, 348.8258, 471.8258, 448.8258, 409.8258, 418.8258, 401.8258, 343.8258, 351.8258, 449.8258, 520.8258, 455.8258, 290.8258, 171.8258, 272.8258, 612.8258, 1021.8258, 1220.8258, 1101.8258, 741.8258, 332.8258, 42.825806, -74.174194, -80.174194, -33.174194, 27.825806, 54.825806, 57.825806, 49.825806, 45.825806, 42.825806, 41.825806, 37.825806, 32.825806])
    #Ar6+ Data

    
    f=.77
    d=1 #half the rise time of normal peak
    t=30
    edges = cfd(signal=spectrum, fraction=f, delay=d, threshold=t)


    plt.clf()
    plt.xlim(0, len(spectrum))
    plt.ylim(0, max(spectrum)+20)
    plt.title("CFD Results (Ar 2+ Data)")
    plt.xlabel("tof (.5ns)")
    plt.ylabel("Amplitude")
    plt.plot(spectrum, '-', color='black', label='original signal')

    peaks, _ = find_peaks(spectrum, prominence=82, wlen=20)
    plt.plot(peaks, spectrum[peaks], "x", color='darkorange', label='peak finder', markersize=12)
    
    for edge in edges[::2]:
        if edge == edges[-2]:
            plt.axvline(edge, color="r", linestyle="--", alpha=.6, label='CFD')
        else:
            plt.axvline(edge, color="r", linestyle="--", alpha=.6)#, label='Ion detected')

            


    plt.legend()
    plt.draw()
    plt.show()
    #print(widths)
    #print(np.mean(widths), np.std(widths))

    

    
