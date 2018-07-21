from template import *

def get_shape(matrix):
	shape = []
	for i in range(len(matrix)):
		if isinstance(matrix[i], list) and isinstance(matrix[i][0], list):
			shape.append(get_shape(matrix[i]))
		elif isinstance(matrix[i], list):
			shape.append(len(matrix[i]))
		else:return shape
	return shape

def Matrix(shape, v=0):
	Y = []
	shape = list(shape)
	for i in range(len(shape)):
		s = shape[i]
		if isinstance(s,list):
			Y.append(Matrix(s))
		else:Y.append([v for k in range(s)])
	if len(Y) == 1:
		Y = Y[0]
	return Y

