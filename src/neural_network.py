from lib.relations import *
from lib.util import *
import math

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
		for i in range(len(shape)):
			s = shape[i]
			x = [0 for i in range(s)]
			self.append(x)
			self.deltas.append(x)
			self.drives.append(x)
			self.biases.append(x)

		self.weights = []
		for i in range(len(self)):
			self.weights.append([])
			for j in range(len(self[i])):
				self.weights[i].append([])
				for k in range(len(self[i-1])):
					self.weights[i][j].append(rr(100)/100)

	def compute_outputs(self, level, X):
		B = self.biases[level]
		Y = []
		for i in range(len(self[level])):
			b = self.biases[level][i]
			y = 0
			for j in range(len(self[level-1])):
				w = self.weights[level][i][j]
				y += self[level-1][j] * w
			Y.append(self.activation(y + b))
		return Y

	def compute_biases(self):
		B = [[-1 for j in range(len(self[i]))] for i in range(len(self))]
		for level in range(len(self.weights)-1):

			for i in range(len(self[level+1])):
				d = self.drives[level+1][i]
				y = self[level+1][i]
				W = self.weights[level+1][i]
				for j in range(len(self[level])):
					w = self.weights[level+1][i][j]
					
					if level == 0:
						x = 1
					else:
						x = self[level][j]
					g = self.drives[level+1][i]
					if y != 0:
					#	if g*w != 0:
						derivative = d*y*w#(g * w / y) * d
						B[level][j] += derivative 

		for i in range(len(B)):
			for j in range(len(B[i])):
				B[i][j] = math.tanh(B[i][j])
		self.biases = B
		return B

	def train(self, reward):
		for level in range(1, len(self)):
			total_output = sum(self[level])
			W = []
			for i in range(len(self.weights[level])):
				W.append([])
				for j in range(len(self.weights[level][i])):
					gi = self.drives[level][i]
					gj = self.drives[level-1][j]
					yi = self[level][i]
					yj = self[level-1][j]
					wij = self.weights[level][i][j]

					xj = yj * wij
					if gj != 0:
						yj *= gj

					dy = yi / total_output
					if reward != 0:
						dg = dy / reward * self.lrate

						W[i].append(gi + dg)

		self.drives = W

	def compute_drives(self, level):
		for i in range(len(self.weights[level])):
			gi = 0
			for j in range(len(self.weights[level][i])):
				gi += self.drives[level-1][j] * self.weights[level][i][j]
			self.drives[level][i] = math.tanh(gi)# += #math.tanh(gi)

	def compute_weights(self):
		W = self.weights
		for level in range(len(self.weights)):
			for i in range(len(self[level])):
				Y = []
				gi = 0
				for j in range(len(self[level-1])):
					yi = self[level][i]
					yj = self[level-1][j]
					dyi = self.deltas[level][i]
					dyj = self.deltas[level-1][j]
					gj = self.drives[level-1][j]

					dw = dyi * dyj 
					if gj != 0: dw *= gj

					W[level][i][j] += dw * self.lrate
		self.weights = W

	def activation(self, x):
		return math.tanh(x)

	def compute_deltas(self, level, V):
		X = self[level]
		D = []
		for i in range(len(V)):
			v = V[i]
			x = X[i]
			d = v-x
			D.append(d)
		return D

	def compute(self, X):
		self.compute_biases()	
		self.compute_weights()

		Y = []
		B = self.biases[0]
		for i in range(len(B)):
			self[0][i] = X[i] + B[i]


		for i in range(1, len(self)):
			X = self[i-1]
			y = self.compute_outputs(i, X)
			d = self.compute_deltas(i, y)
			self[i] = x
			self.deltas[i] = d
			Y = y
		return Y

nn=NeuralNetwork([10, 13, 10])

X = [[1, 0, 1, 1, 0, 0, 1, 0, 0, 0],
	 [0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
	 [0, 0, 1, 0, 0, 0, 0, 1, 1, 0],
	 [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
	 [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
	 [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
	 [0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
	 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
	 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

Y = []



log = open('log.txt', 'w')
c = -1

rewards = [[1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
		   [-1, 1, -1, -1, -1, -1, -1, -1, -1, -1],
		   [-1, -1, 1, -1, -1, -1, -1, -1, -1, -1],
		   [-1, -1, 1, -1, -1, -1, -1, -1, -1, -1],
		   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
		   [-1, -1, -1, 1, -1, -1, -1, -1, -1, -1],
		   [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
		   [-1, -1, -1, 1, -1, -1, -1, -1, -1, -1],
		   [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1],
		   [-1, -1, -1, -1, -1, -1, -1, -1, 1, -1]]


for i in range(10000):
	for j in range(len(X)):
		x = X[j]
		c += 1
		nn.drives[0] = rewards[j]
		Y = nn.compute(x)
		Y = reverse(sort(Y))
		# index = round(len(Y) * j/len(X))

		# y=sort(Y)
		# index = y.index(index) / len(y)
		# reward = index -0.5
		# nn.train(reward)


		# R = rewards[j]
		# for l in range(len(R)):
		# 	R[l] *= x[l]
		# r = sum(R)
		# nn.train(r)
		# if j == 0:
		# 	if sort(Y)[0] == 0:
		# 		nn.train(1)
		# 	else:
		# 		nn.train(-1)

		s = ''
		# if j == 1:
		# Y = sort(Y)
		for k in range(len(Y)):
			y = Y[k]
			s += str(y) + '	'
		print(s)
		log.write(str(c) + '	' + s + '\n')
	print()