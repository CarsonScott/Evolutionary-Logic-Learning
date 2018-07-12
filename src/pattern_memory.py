from lib.util import *
from matrix import *

def Pow(X=[]):
	return X[0] ** X[1]
def In(X=[]):
	return X[0] in X[1]
def mul(X=[]):
	y = 1
	for x in X:
		y *= x
	return y
def add(X=[]):
	y = 0
	for x in X:
		y += x
	return y
def sub(X=[]):
	y = X[0]
	del X[0]
	for x in X:
		y -= x
	return y
def div(X=[]):
	y = X[0]
	del X[0]
	for x in X:
		y /= x
	return y
def And(X=[]):
	for x in X:
		if x != True:
			return False
	return True
def Or(X=[]):
	for x in X:
		if x == True:
			return True
	return False
def Not(X=[]):
	for x in X:
		if x == True:
			return False
	return True
	
def eq(X=[]):
	for i in range(1, len(X)):
		if X[i-1] != X[i]:return False
	return True
def neq(x):
	for i in range(1, len(X)):
		if X[i-1] == X[i]:return False
	return True
def gt(X=[]):
	for i in range(1, len(X)):
		if X[i-1] <= X[i]:
			return False
	return True
def lt(X=[]):
	for i in range(1, len(X)):
		if X[i-1] >= X[i]:
			return False
	return True
def gteq(X=[]):
	for i in range(1, len(X)):
		if X[i-1] < X[i]:
			return False
	return True
def lteq(X=[]):
	for i in range(1, len(X)):
		if X[i-1] > X[i]:
			return False
	return True
def get(X=[]):
	x = X[0]
	k = X[1]
	return x[k]
def set(X=[]):
	x = X[0]
	k = X[1]
	v = X[2]
	x[k] = v
	return x

class string(str):
	pass

class PatternMemory(Dict):
	def __init__(self):
		super().__init__()
		self.initialize()
	def __setitem__(self, key, value):
		type = self.identify(value)
		super().__setitem__(key, value)
	def initialize(self):
		self['+'] = add
		self['-'] = sub
		self['*'] = mul
		self['/'] = div
		self['^'] = pow
		self['>'] = gt
		self['<'] = lt
		self['='] = eq
		self['!='] = neq
		self['>='] = gteq
		self['<='] = lteq
		self['&'] = And
		self['in'] = In
		self['!'] = Not
		self['|'] = Or
		self['id'] = identify
		self['mat'] = Matrix
		self['true'] = True
		self['false'] = False

	def identify(self, value):
		type = 'data'
		if isinstance(value, tuple):
			type = 'pattern'
		if isinstance(value, string):
			type = 'string'
		elif isinstance(value, list):
			type = 'list'
		elif isinstance(value, str):
			type = 'key'
		elif isinstance(value, bool):
			type = 'bool'
		elif callable(value):
			type = 'op'
		return type

	def translate(self, value):
		type = self.identify(value)
		output = value
		if type == 'key':
			output = self[value]
		elif type == 'list':
			output = []
			for i in range(len(value)):
				data = self.translate(value[i])
				output.append(data)
		if output != None:
			return output

	def compute(self, pattern):
		output = pattern
		type = self.identify(pattern)
		if type == 'template':
			inputs = self.translate(pattern['data'])
			function = self.translate(pattern['type'])
			output = function()

			inputs = list()
			function = self.translate(pattern['type'])
			for i in range(1, len(pattern)):
				value = self.translate(pattern['data'][i])
				inputs.append(self.compute(value))
			output = function(inputs)

		if type == 'pattern':
			inputs = list()
			types = list()
			matrices = list()
			indices = list()
			function = self.translate(pattern[0])
			for i in range(1, len(pattern)):
				value = self.translate(pattern[i])
				input = self.compute(value)
				type = self.identify(input)
				inputs.append(input)
				types.append(type)
				if type == 'matrix':
					matrices.append(input)
					indices.append(i-1)

			Y = None
			if len(matrices) > 1:
				matrices = associate(*matrices)
				data = [list(inputs) for i in range(len(matrices))]
				for i in range(len(matrices)):
					for j in range(len(matrices[i])):
						x = matrices[i][j]
						k = indices[j]
						data[i][k] = x
				Y = Matrix()
				for i in range(len(data)):
					Y.append(function(data[i]))
			elif len(matrices) > 0:
				Y = Matrix()
				matrix = matrices[0]
				index = indices[0]
				data = [list(inputs) for i in range(len(matrix))]
				for i in range(len(matrix)):
					data[i][index] = matrix[i]
				for i in range(len(data)):
					Y.append(function(data[i]))
					
			else: Y = function(inputs)
			return Y

		elif type == 'list':
			output = []
			for i in range(len(pattern)):
				output.append(self.translate(pattern[i]))
		elif type == 'str':
			value = self.translate(pattern)
			output = self.compute(value)
		return output

	def compress(self, pattern):
		output = self.translate(pattern)
		type = self.identify(pattern)
		if type == 'pattern':
			inputs = list()
			function = pattern[0]
			for i in range(1, len(pattern)):
				value = self.translate(pattern[i])
				if self.identify(value) == 'pattern':
					value = self.compress(value)
				else:
					value = pattern[i]
				inputs.append(value)
			output = tuple([function] + inputs)
		return output

	def convert(self, data):
		type = self.identify(data)
		output = None
		if type == 'pattern':
			model = Dict()
			model['f'] = data[0]
			for i in range(1, len(data)):
				key = 'x' + str(i-1)
				value = data[i]
				type = self.identify(value)
				if type == 'pattern':
					value = self.convert(value)
				model[key] = value	
			output = model

	def __call__(self, data):
		return self.compute(self.translate(data))


if __name__ == "__main__":

	# Memory
	memory = PatternMemory()


	memory['get'] = get
	memory['set'] = set
	memory['store'] = memory.__setitem__

	# Variables
	memory['a'] = ('*', 'b', 'c')
	memory['b'] = 3
	memory['c'] = 2
	memory['d'] = 66
	memory['e'] = -2


	y = memory.convert('a')
	print(y)
	# Structures
	memory['pattern'] = ('*', 'a', 'd')
	memory['model'] = memory.convert(memory.translate('pattern'))
	y = memory(('get', 'model', string('f')))
	print(y)
	# print(memory.compress(memory.translate('pattern')))