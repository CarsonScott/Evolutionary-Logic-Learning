from tree import *
from inspect import signature


class string(str):
	pass

class PatternMemory(Dict):
	def __init__(self):
		self.types = Dict()
	def __setitem__(self, key, value):
		type = self.identify(value)
		self.set_type(key, type)
		super().__setitem__(key, value)

	def get_type(self, key):
		return self.types[key]
	def set_type(self, key, type):
		self.types[key] = type

	def identify(self, value):
		type = 'data'
		if isinstance(value, tuple):
			type = 'pattern'
		if isinstance(value, dict):
			type = 'model'
		if isinstance(value, string):
			type = 'string'
		elif isinstance(value, list):
			type = 'list'
		elif isinstance(value, str):
			type = 'key'
		elif callable(value):
			type = 'op'
		return type

	def translate(self, value, scope=None):
		if scope == None:scope = self
		type = self.identify(value)
		output = value
		if type == 'key':
			output = self.translate(scope[value])
		elif type == 'list':
			output = []
			for i in range(len(value)):
				data = self.translate(value[i])
				output.append(data)
		return output

	def compute(self, pattern):
		output = pattern
		type = self.identify(pattern)
		if type == 'pattern':
			inputs = list()
			function = self.translate(pattern[0])
			for i in range(1, len(pattern)):
				value = self.translate(pattern[i])
				inputs.append(self.compute(value))
			params = len(signature(function).parameters)
			if params > 1: output = function(*inputs)
			else: output = function(inputs)
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
		elif type == 'model':
			pattern = [data['f']]
			print(data.keys())
			for i in range(1, len(data)):
				key = 'x' + str(i-1)
				value = data[key]
				type = self.identify(value)
				if type == 'model':
					value = self.convert(value)
				pattern.append(value)
			output = tuple(pattern)
		return output

	def __call__(self, data):
		return self.compute(self.translate(data))

def mul(X):
	y = 1
	for x in X:
		y *= x
	return y
def add(X):
	y = 0
	for x in X:
		y += x
	return y
def sub(X):
	y = X[0]
	del X[0]
	for x in X:
		y -= x
	return y
def div(X):
	y = X[0]
	del X[0]
	for x in X:
		y /= x
	return y

def eq(X):
	for i in range(1, len(X)):
		if X[i-1] != X[i]:return False
	return True
def neq(x):
	for i in range(1, len(X)):
		if X[i-1] == X[i]:return False
	return True
def gt(X):
	for i in range(1, len(X)):
		if X[i-1] <= X[i]:
			return False
	return True
def lt(X):
	for i in range(1, len(X)):
		if X[i-1] >= X[i]:
			return False
	return True
def gteq(X):
	for i in range(1, len(X)):
		if X[i-1] < X[i]:
			return False
	return True
def lteq(X):
	for i in range(1, len(X)):
		if X[i-1] > X[i]:
			return False
	return True
def get(X):
	x = X[0]
	k = X[1]
	return x[k]
def set(X):
	x = X[0]
	k = X[1]
	v = X[2]
	x[k] = v
	return x

# Memory
memory = PatternMemory()

# Operators
memory['+'] = add
memory['-'] = sub
memory['*'] = mul
memory['/'] = div
memory['^'] = pow
memory['>'] = gt
memory['<'] = lt
memory['='] = eq
memory['!='] = neq
memory['>='] = gteq
memory['<='] = lteq

memory['get'] = get
memory['set'] = set
memory['store'] = memory.__setitem__

# Variables
memory['a'] = ('*', 'b', 'c')
memory['b'] = 3
memory['c'] = 2
memory['d'] = 66
memory['e'] = -2

# Structures
memory['pattern'] = ('*', 'a', 'd')
memory['model'] = memory.convert(memory.translate('pattern'))
y = memory(('get', 'model', string('f')))
print(memory.compress(memory.translate('pattern')))