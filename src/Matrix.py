from lib.util import *

def create(*X):
	if len(X) == 1:X = X[0]
	return Matrix(list(X))
def to_matrix(*X):
	Y = Matrix()
	if iterable(X):
		if len(X) == 1:X = X[0]
		return Matrix(X)

class Matrix(list):
	def __getitem__(self, X):
		if iterable(X):
			index = X[1:]
			data = super().__getitem__(X[0])
			if len(index) == 1:
				index = index[0]
			return data[index]
		else:return super().__getitem__(X)
	def combine(*X):
		if len(X) == 1:X = X[0]
		if iterable(X):
			Y = Matrix()
			for x in X:
				if iterable(x):
					Y += x
				else:
					Y.append(x)
			return Y
	def associate(*X):
		Y = Matrix()
		if len(X) == 1:X = X[0]
		for i in range(len(X[0])):
			y = [X[j][i] for j in range(len(X))]
			Y.append(y)
		return Y
	def distribute(*X):
		v = X[0]
		if not iterable(v):
			v = [v]
		Y = Matrix()
		for j in range(1, len(X)):
			y = Matrix(X[j])
			if iterable(y):
				for i in range(len(y)):
					y[i] = to_matrix(y[i], v)
			Y.append(y)
		if len(Y) == 1:
			Y = Y[0]
		return Y
	def reverse(self):
		return reverse(self)

class Function(Matrix):
	def __init__(self, matrix=[]):
		super().__init__(matrix)
		self.indices = Dict()
		for i in range(len(matrix)):
			x,y = matrix[i]
			self.set(x, y)
	def get(self, input):
		if input in self.indices.keys():
			return self.indices[input]
		return input
	def set(self, input, output):
		index = len(self)
		self.append(create(input, output))
		if input not in self.indices.keys():
			self.indices[input] = create()	
		self.indices[input].append(index)
	def index(self, input):
		index = self.get(input)
		return index
	def output(self, index):
		output = self[index, 1]
		return output
	def __call__(self, input):
		indices = self.index(input)
		outputs = Matrix()
		for i in indices:
			output = self.output(i)
			outputs.append(output)
		if len(outputs) == 1:
			outputs = outputs[0]
		return outputs

if __name__ == "__main__":
	A = create([1, 1, 1])
	B = create([2, 2, 2])
	C = create([3, 3, 3])
	D = A.associate(A, B, C)
	E = D.associate([4, 4, 4])
	y = A.distribute(D)

	X = Function()

	X.set(0, 111)
	X.set(1, 1214)
	X.set(0, 2135)

	print(X(0))