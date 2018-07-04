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

	def create(self, *data):
		values = list(data)
		size = len(values)
		if size > 0:key = values[0]
		if size >= 1:function = values[1]
		if size >= 2:inputs = values[2:]
		self[key] = Operator(function, inputs)

	def translate(self, data):
		dtype = identify(data)
		if isinstance(data, Operator): dtype = 'operator'
		elif isinstance(data, list): dtype = 'list'
		elif data in self.keys(): dtype = 'key'
		output = data
		if dtype == 'operator':
			function = self.translate(data[0])
			inputs = self.translate(data[1:])
			print(function, inputs)
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

# dm = DynamicMemory()
# dm['multiply'] = Mult
# dm['*'] = 'multiply'

# dm['divide'] = Div
# dm['/'] = 'divide'

# dm['a'] = 4
# dm['b'] = 3
# dm['c'] = 12

# dm.create('X', '*', 'a', 'b', 'c')
# print(dm.translate('X'))

