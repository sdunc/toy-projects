# stephen dunc
# abelian sandpile

import numpy as np
import random
from PIL import Image
import sys

# Override recursion depth limit for when the sand pile collapses
sys.setrecursionlimit(20000)
#print(sys.getrecursionlimit())

class Sandpile:
	def __init__(self, d):
		self.d = d
		self.pile = np.zeros((self.d,self.d), dtype=int)

	def get_d(self):
		return len(self.pile)

	def add_grain_to_pile(self, x, y):
		if x <= self.d-1 and x >= 0 and y <= self.d-1 and y >= 0:
			pile_value = self.pile[x][y]
			if pile_value < 3:
				#easy case, no spilling
				self.pile[x][y] += 1
			elif pile_value == 3: #should never have a case when > 3 
				#set back to 0
				self.pile[x][y] = 0
				self.add_grain_to_pile(x+1,y)
				self.add_grain_to_pile(x-1,y)
				self.add_grain_to_pile(x,y+1)
				self.add_grain_to_pile(x,y-1)

	def save_image(self):
		#create a new image object with the right dimensions
		I = Image.new('RGBA', (self.d, self.d))
		IM = I.load()
		for x in range(len(self.pile)-1):
			for y in range(len(self.pile)-1):
				val = self.pile[x][y]
				if val == 0:
					IM[x,y] = (255,255,178)
				if val == 1:
					IM[x,y] = (254,204,92)			
				if val == 2:
					IM[x,y] = (253,141,60)
				if val == 3:
					IM[x,y] = (227,26,28)
		I.save('sandpile' + ".png", "PNG")
		print("Image saved!")

s = Sandpile(400)

point1_x = 75
point1_y = 60
mid = s.get_d()//2

#point2_x = 75
#point2_y = 77

for x in range(100000):
	#s.add_grain_to_pile(point1_x, point1_y)
	#if point1_y <= 90:
#		point1_y +=1 
#	else:
#		point1_y = 60

#	if x % 2 == 0:
#		s.add_grain_to_pile(point1_x, point1_y)
#	else:
	
	#s.add_grain_to_pile(random.randint(0,s.get_d()-1), random.randint(0,s.get_d())-1)
	#OR alwats add to the center of the pile?
	s.add_grain_to_pile(mid, mid)
s.save_image()
