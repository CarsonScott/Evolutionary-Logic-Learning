from template import *
from phrase import *
from goodata import *

def Mult(X):
	y = None
	for x in X:
		if y == None:
			y = x
		else:y *= x
	return y

def Div(X):
	y = None
	for x in X:
		if y == None:
			y = x
		else:y /= x
	return y

class DynamicMemory(Dict):

	def create(self, key, *data):
		data = list(data)
		if len(data) == 1 and isinstance(data[0], list):
			data = data[0]
		operator = None
		inputs = None
		if len(data) > 0:
			operator = data[0]
			if len(data) > 1:
				inputs = data[1:]
		self[key] = Operator(operator, inputs)

	def translate(self, data):
		dtype = identify(data)
		if isinstance(data, Operator): dtype = 'operator'
		elif isinstance(data, list): dtype = 'list'
		elif data in self.keys(): dtype = 'key'
		output = data
		if dtype == 'operator':
			function = self.translate(data[0])
			inputs = self.translate(data[1:])
			output = function(inputs)
		elif dtype == 'list':
			output = list()
			for i in range(len(data)):
				value = self.translate(data[i])
				output.append(value)
		elif dtype == 'key':
			output = self.translate(self[data])
		return output

class Operator(list):
	def __init__(self, function, inputs):
		self.function = function
		self.inputs = inputs
		ftype = identify(function)
		xtype = identify(inputs)
		if ftype != 'none':
			self.append(function)
		if xtype != 'none':
			if xtype == 'list':
				for x in inputs:
					self.append(x)
			else:self.append(inputs)

dm = DynamicMemory()
dm['multiply'] = Mult
dm['*'] = 'multiply'

dm['divide'] = Div
dm['/'] = 'divide'

dm['a'] = 4
dm['b'] = 3
dm['c'] = 12

dm['X'] = Operator('*', ['a', 'b', 'c'])
dm['Y'] = Operator('/', ['a', 'b', 'c'])

dm.create('Z', 'multiply', 'X', 'Y')

print(dm.translate('Z'))

