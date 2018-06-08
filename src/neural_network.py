from lib.relations import *
import math
from lib.util import *


def multiply(X, Y):
	return [X[i] * Y[i] for i in range(len(X))]
def subtract(X, Y):
	return [X[i] - Y[i] for i in range(len(X))]

def softmax(x):
	return math.log(1 + math.exp(x))
def logistic(x):
  return 1 / (1 + math.exp(-x))


class NeuralNetwork(list):

	def __init__(self, shape):
		shape = shape
		self.weights = []
		self.biases = []
		self.deltas = []
		self.drives = []
		self.lrate = 0.001
		self.init(shape)

	def init(self, shape):
		i = 0
		for s in shape:
			x = [0 for i in range(s)]
			self.append(x)
			self.deltas.append(x)
			self.biases.append(x)
			self.drives.append(x)
		for i in range(len(self)):
			self.weights.append([]) 
			for j in range(len(self[i])):
				self.weights[i].append([rr(100)/100 for k in range(len(self[i-1]))])

	def compute_outputs(self, level, X):
		B = self.biases[level]
		W = self.weights[level]
		Y = []
		for i in range(len(self[level])):
			y = sum(multiply(W[i], X))
			b = B[0]
			Y.append(self.activation(y + b))
		return Y

	def compute_biases(self, level, X):
		for i in range(len(self[level])):
			W = self.weights[level][i]
			B = []
			b = 0
			for j in range(len(W)):
				w = W[j]
				x = X[j]
				b += w * x
			B.append(b)
		return B

	def compute_weights(self, level):
		W = []
		for i in range(len(self[level])):
			W.append(self.weights[level][i])
			Y = []
			for j in range(len(W)):
				gj = self.drives[level-1][j]
				yi = self[level][i]
				dyj = self.deltas[level-1][j]
				r = -gj
				dw = r * yi * dyj
				W[i][j] += dw * self.lrate
		return W

	def activation(self, x):
		return softmax(x)

	def compute_deltas(self, level, V):
		X = self[level]
		D = []
		for i in range(len(X)):
			v = V[i]
			x = X[i]
			d = v-x
			D.append(d)
		return D

	def compute(self, X):
		Y = []
		self[0] = X
		for i in range(1, len(self)):
			X = self[i-1]
			b = self.compute_biases(i, X)
			y = self.compute_outputs(i, X)
			d = self.compute_deltas(i, y)
			w = self.compute_weights(i)
			self[i] = x
			self.biases[i] = b
			self.deltas[i] = d
			self.weights[i] = w
			Y.append(y)
		return Y


nn=NeuralNetwork([10, 10, 10])

X = [[0, 1, 0, 0, 1, 1, 0, 1, 1, 0],
	 [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
	 [0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
	 [1, 0, 0, 1, 0, 0, 0, 1, 1, 1]]

for x in X:
	print(nn.compute(x))