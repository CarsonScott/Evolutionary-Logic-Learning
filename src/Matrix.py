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
def execute(f, X):
	return [f(x) for x in X]

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
	# if not isinstance(shape, list):

	if isinstance(shape, int):
		shape = [i for i in range(shape)]
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
