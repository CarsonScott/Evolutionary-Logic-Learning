from lib.util import *

def multiply(X, Y):
	return [X[i] * Y[i] for i in range(len(X))]

class MemorySystem:

	def __init__(self, patterns=[], delay=1):
		super().__init__()
		self.goals = []
		self.ratings = []
		self.biases = []
		self.outputs = []
		self.previous = []
		self.weights = []
		self.average = []
		self.lrate = .1
		self.time = 0
		self.delay = delay
		self.state = 0
		for i in range(len(patterns)):
			self.patterns.append(patterns[i])
			self.goals.append(0)
			self.biases.append(0)
			self.average.append(0)
			self.outputs.append(0)
			self.ratings.append(0)
			self.previous.append([0 for j in range(len(patterns))])
			self.weights.append([0 for j in range(len(patterns))])
			
	def set_goal(self, i):
		self.goals[i] = True
	
	def remove_goal(self, i):
		self.goals[i] = False

	def get_attitude(self, i):
		if self.goals[i]:
			return -1
		return 1

	def compute_rating(self, i, j):
		s = self.get_state(i)
		r = self.get_attitude(i)
		return s*r

	def compute_biases(self, data):
		biases = []
		for i in range(len(self.weights)):
			b = 0
			for j in range(len(self.weights)):
				wi = self.weights[i][j]
				x = data[str(j)]
				b += wi * x
			biases.append(b)
		return biases


	def compute_weights(self, data):
		weights = []
		for i in range(len(self.outputs)):
			ri = -1
			if data[str(i)]:
				ri = 1
			W = self.weights[i]
			for j in range(len(W)):
				dyj = -self.get_delta(j)
				yi = self.outputs[i]
				rj = self.get_attitude(j)

				if self.goals[j] and i != j:
					dw = ri * dyj * self.lrate
					W[j] += dw
			weights.append(W)
		return weights

	def compute_output(self, X, i):
		r = self.get_attitude(i)
		y = self.patterns[i](X) * r
		return y

	def compute_outputs(self, X):
		outputs = []
		for i in range(self.size()):
			b = self.biases[i]
			y = self.compute_output(X, i) + b
			outputs.append(tanh(y))
		return outputs

	def get_delta(self, i):
		p = self.average[i]
		y = self.outputs[i]
		return y-p

	def compute_averages(self):
		Y = []
		for i in range(len(self.previous[0])):
			Y.append(0)
			for j in range(len(self.previous)):
				Y[i] += self.previous[j][i]
		return Y

	def compute(self, X):
		self.previous.append(list(self.outputs))
		
		self.time += 1
		if self.time >= self.delay:
			self.time = 0

			self.average = self.compute_averages()
			self.previous = []

			self.biases = self.compute_biases(X)
			self.outputs = self.compute_outputs(X)
			self.weights =  self.compute_weights(X)
