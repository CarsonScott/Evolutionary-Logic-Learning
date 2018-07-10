from function import *

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
		return 0
	def reset(self):
		self.examples = 0
		for i in self.keys():
			self[i] = 0

class AssociativeMemory(Probability):
	def __init__(self, keys, size):
		self.scores = Dict()
		self.times = Dict()
		self.lrate = 0.01
		self.weights = Dict()
		self.output = Dict()
		for i in range(len(keys)):
			k = keys[i]
			# self.scores[k] = rr(100)/100
			self.times[k] = 0
			self.output[k] = 0
			self.weights[k] = Dict()
			for j in range(len(keys)):
				self.weights[k][keys[j]] = rr(100)/1000
			self[k] = Probability(keys)
		self.buffer = Matrix()
		self.examples = 1
		self.capacity = size

	def append(self, keys):
		self.buffer.append(keys)
		self.times[keys] = -self.capacity
		error = self.capacity-len(self.buffer)
		if error > 0:del self.buffer[0:len(self.buffer)-self.capacity-1]

		for i in range(len(self.keys())):
			ki = self.keys()[i]
			self.output[ki] = self.compute(ki)
			Bi = ki in self.buffer
			for j in range(i, len(self.keys())):
				if i != j:
					kj = self.keys()[j]
					w = self.scores[ki]
					y = self.output[ki]
					Bj = kj in self.buffer

					if Bi and Bj:
						bi = self.buffer.index(ki)
						bj = self.buffer.index(kj)

						most_recent
						if bi < bj:most_recent = kj
						else:most_recent = ki

						if most_recent == ki:
							self.weights[ki]

					self[ki].append(y, w)

	def compute(self):
		for i in self.keys():
			for j in self.keys():
				self.outputs[i] = self[i].compute(j)

		outputs = Dict()
		for i in self[keys].keys():
			outputs[i] = self[keys].compute(i)
		return outputs

	def update(self):
		for ki in self.keys():
			self.times[ki] += 1
			for kj in self.keys():
				outputs = self[ki].compute(kj)
				self.scores[kj] += outputs * logistic(-self.times[kj]) * self.lrate
		return self.scores