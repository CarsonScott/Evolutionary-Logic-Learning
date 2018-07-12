from lib.util import *
from matrix import *

class Pattern(Dict):
	def __init__(self, size, keys):
		self.biases = Dict()
		self.weights = Dict()
		self.predictions = list()
		self.active = list()
		self.size = size
		self.fitness = 0
		self.performance = 0
		self.threshold = 0
		self.lrate = 0.01
		for key in keys:
			self.biases[key] = rr(1, 10)/1000
			self.weights[key] = Dict()
			for k in keys:
				self.weights[key][k] = rr(1, 10)/1000

	def compute_output(self, key):
		x = key in self.active
		b = self.biases[key]
		y = x * b
		return y

	def compute_performance(self, key):
		if key in self.predictions:
			index = self.predictions.index(key)
		else:index = -1
		performance = self.biases[key] * logistic(index)
		return performance

	def compute_fitness(self):
		fitness = self.fitness + self.lrate * self.performance * softmax(-abs(self.fitness))
		return fitness

	def input(self, key):
		if key in self.active:
			del self.active[self.active.index(key)]
		self.active.append(key)
		if len(self.active) > self.size:
			del self.active[0:len(self.active)-self.size]
		self.performance = self.compute_performance(key)
		self.fitness = self.compute_fitness()
	
	def compute(self):
		Y = Dict()
		outputs = Dict()
		for key in self.biases.keys():
			W = self.weights[key]
			y = self.compute_output(key)
			for i in self.weights[key].keys():
				if i != key:
					if i not in Y.keys():
						Y[i] = W[i] * y
					else:Y[i] += W[i] * y
		for key in Y.keys():
			y = tanh(Y[key]/len(Y.keys()))
			self.biases[key] += self.lrate * y * tanh(1-abs(self.biases[key]))
		self.predictions = sort(Y)[len(Y)-self.size:len(Y)]
		return Y

	def update(self):
		for i in range(len(self.active)):
			key = self.active[i]
			for j in range(i, len(self.active)):
				if i != j:
					k = self.active[j]
					y = tanh(1-(j - i)/(self.size))
					self.weights[key][k] += self.lrate * y * tanh(1-abs(self.weights[key][k]))

	def __call__(self, x):
		if x in self.biases.keys():
			P = Matrix(self.predictions)
			M = Matrix(self.active)
			self.input(x)
			F = self.performance
			self.compute()
			self.update()
			return self.record(F, M, P)

	def record(self, performance, active, predicted):
		record = Dict()
		record['performance'] = performance
		record['predicted'] = predicted
		record['active'] = active
		return record

class NumericalPattern(Pattern):
	def __init__(self, size, r, b):
		keys = []
		if identify(r) == 'int':
			for i in range(int(int(r/b))):
				keys.append(str(int(i*b)))
		elif iterable(r):
			for i in range(r[0], r[1]):
				keys.append(str(int(i*b)))
		keys.append(str(int(keys[len(keys)-1]) + b))
		print(keys)
		super().__init__(size, keys)

	def input(self, value):
		keys = self.biases.keys()
		key = None
		for i in range(len(keys)-1):
			k1 = keys[i]
			k2 = keys[i+1]
			if int(k1) <= value < int(k2):
				if abs(int(k1) - value) >= abs(int(k2) - value):
					key = str(k2)
				else:key = str(k1)
		super().input(str(key))