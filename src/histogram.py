import math
from lib.util import * 

def bump(x):
	if x == 0:return 1
	return math.exp(-1/(1-pow(x,2))) / bump(0)

class Histogram(list):
	def __init__(self, value_range):
		self.inc = 0.01
		self.log = Dict()
		self.size = value_range

	def retrieve(self, index):
		if isinstance(index, float):
			index = round(index*10)
		if index not in self.log.keys():
			if len(self.log.keys()) < self.size:
				self.log[index] = 0
		if index in self.log.keys():
			return index

	def update(self, index):
		index = None
		if isinstance(index, float):
			index = round(index)
		if index in self.log.keys():
			self.log[index] += self.inc * logistic(-self.log[index])
