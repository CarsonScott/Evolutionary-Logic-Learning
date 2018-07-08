from matrix import *

class Probability(Dict):
	def __init__(self, keys):
		self.examples = 0
		for i in range(len(keys)):
			k = keys[i]
			self[k] = 0
	def append(self, keys, weight=1):
		for i in range(len(keys)):
			k = keys[i]
			self[k] += weight
		self.examples += 1
	def compute(self, key):
		size = self.examples
		if size != 0:
			return tanh(self[key]/size)
	def reset(self):
		self.examples = 0
		for i in self.keys():
			self[i] = 0

class JointProbability(Probability):
	def __init__(self, keys, size):
		for i in range(len(keys)):
			k = keys[i]
			self[k] = Probability(keys)
		self.buffer = Matrix()
		self.examples = 0
		self.capacity = size

	def append(self, keys):
		self.buffer.append(keys)
		del self.buffer[0:len(self.buffer)-self.capacity]
		for i in range(len(self.buffer)):
			x = self.buffer[i]
			for j in range(i, len(self.buffer)):
				if i != j:
					w = 1
					if len(self.buffer) > 0:
						w = tanh(1-abs(i-j)/self.capacity)
					y = self.buffer[j]
					self[x].append(y, w)
				
	def compute(self, keys):
		outputs = Dict()
		for i in self[keys].keys():
			outputs[i] = self[keys].compute(i)
		return outputs