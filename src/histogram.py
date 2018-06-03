import math

def bump(x):
	if x == 0:return 1
	return math.exp(-1/(1-pow(x,2))) / bump(0)

class Histogram(list):
	def __init__(self, size):
		self.inc = 0.04
		self.dec = 0.01
		for i in range(size):
			self.append(0)

	def add(self, sample):
		index = round(sample)
		if index in range(0, len(self)):
			self[index] += self.inc * bump(-self[index]) 
			self[index] -= self.dec * bump(self[index]) 