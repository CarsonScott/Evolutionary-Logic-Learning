from lib.util import *
import functools, operator

def create(*X):
	if len(X) == 1:X = X[0]
	return Matrix(list(X))
def to_matrix(*X):
	Y = Matrix()
	if len(X) == 1:X = X[0]
	if iterable(X):
		for x in X:
			Y.append(to_matrix(x))
	else:
		Y = [X]
	return Matrix(Y)
def combine(*X):
	if len(X) == 1:X = X[0]
	if iterable(X):
		Y = Matrix()
		for x in X:
			if iterable(x):
				Y += x
			else:Y.append(x)
		return Y
def associate(*X):
	Y = Matrix()
	if iterable(X[0]):
		size = len(X[0])
		for i in range(size):
			y = Matrix([X[j][i] for j in range(len(X))])
			if len(y) == 1:
				y = y[0]
			Y.append(y)
	if len(Y) == 1:
		return Y[0]
	return Matrix(Y)
def distribute(*X):
	v = X[0]
	if not iterable(v):
		v = v
	Y = Matrix()
	for j in range(1, len(X)):
		y = Matrix(X[j])
		if iterable(y):
			for i in range(len(y)):
				if iterable(y[i]):
					y[i] = create(*y[i], v)
				else:y[i] = create(y[i], v)
		Y.append(y)
	if len(Y) == 1:
		Y = Y[0]
	return Y
class Matrix(list):
	def __getitem__(self, X):
		if iterable(X):
			index = Matrix(X[1:])
			data = super().__getitem__(X[0])
			if len(index) == 1:
				index = index[0]
			return data[index]
		else:return super().__getitem__(X)
	def __add__(self, X):
		Y = Matrix()
		X = associate(self, X)
		for i in range(len(X)):
			x = None
			y = 0
			for j in range(len(X[i])):
				if iterable(X[i][j]):
					if iterable(y):
						x = y + Matrix(X[i][j])
					else:x = Matrix(X[i][j])
				else:
					if not iterable(y) and y != None:
						x = y + X[i][j]
					else:x = X[i][j]
				y = x
			Y.append(y)
		return Y
	def __mul__(self, X):
		Y = Matrix()
		X = associate(self, X)
		for i in range(len(X)):
			x = None
			y = None
			for j in range(len(X[i])):
				if iterable(X[i][j]):
					if iterable(y):
						x = y * Matrix(X[i][j])
					else:x = Matrix(X[i][j])
				else:
					if not iterable(y) and y != None:
						x = y * X[i][j]
					else:x = X[i][j]
				y = x
			Y.append(y)
		return Y
def compose(shape, value=0):
	Y = Matrix()
	for i in range(len(shape)):
		s = shape[i]
		if iterable(s):
			y = compose(s, value)
		elif s != 0:y = [value for j in range(s)]
		else:y = value
		Y.append(y)
	return Y
def shape(matrix):
	size = len(matrix)
	leaf = True
	output = [0 for i in range(size)]
	for i in range(size):
		if iterable(matrix[i]):
			output[i] = shape(Matrix(matrix[i]))
			leaf = False
	if leaf:return size
	return Matrix(output)

y = Matrix([1, 2, 3, [3,4,[89, [3]]]])

y = shape(y)
y = compose(shape(y), 2)
print(compose(shape(y), 4))
# a = Matrix([2, 2, 5, 7])
# b = Matrix([1, 43])
# c = Matrix([3, 4, 3, 2])

# print('reverse(a)')
# print(reverse(a))
# print('combine(a, b)')
# print(combine(a, b))
# print('associate(a, c)')
# print(associate(a, c))
# print('combine(a, b)')
# print(combine(a, b))
# print('distribute(a, b)')
# print(distribute(a, b))
# print(create([2, 3], 3) + create([1, 2], 3), '\n\n')
# print(create(4, [2, 3]) + create(3, [1, 2]), '\n\n')
# print(a + c, '\n\n')

# class Function(Matrix):
# 	def __init__(self, matrix=[]):
# 		super().__init__(matrix)
# 		self.indices = Dict()
# 		for i in range(len(matrix)):
# 			x,y = matrix[i]
# 			self.set(x, y)
# 	def get(self, input):
# 		if input in self.indices.keys():
# 			return self.indices[input]
# 		return input
# 	def set(self, input, output):
# 		index = len(self)
# 		self.append(create(input, output))
# 		if input not in self.indices.keys():
# 			self.indices[input] = create()	
# 		self.indices[input].append(index)
# 	def index(self, input):
# 		index = self.get(input)
# 		return index
# 	def output(self, index):
# 		output = self[index, 1]
# 		return output
# 	def __call__(self, input):
# 		indices = self.index(input)
# 		outputs = Matrix()
# 		for i in indices:
# 			output = self.output(i)
# 			outputs.append(output)
# 		if len(outputs) == 1:
# 			outputs = outputs[0]
# 		return outputs

# if __name__ == "__main__":
# 	A = create([1, 1, 1])
# 	B = create([2, 2, 2])
# 	C = create([3, 3, 3])
# 	D = associate(A, B)
# 	print(D)
# 	E = distribute(to_matrix(54), D)
# 	print(E)
# 	# # E = D(associate, [4, 4, 4])
# 	# y = A(distribute, D)
# 	# print(y)
# 	X = Function()

# 	X.set(0, 111)
# 	X.set(1, 1214)
# 	X.set(0, 2135)

# 	print(X(0))