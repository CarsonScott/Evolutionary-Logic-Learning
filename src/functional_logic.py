from dictionary import *
from lib.relations import *

def copy(X):
	if isinstance(X, list):
		Y = type(X)()
		for x in X:
			Y.append(x)
		return Y
	elif isinstance(X, dict):
		Y = type(X)()
		for i in list(X.keys()):
			x = X[i]
			Y[i] = x
		return Y
	else:return X
def create_dict(K, V=[]):
	Y = Dictionary()
	for j in range(len(K)):
		i = K[j] 
		if isinstance(V, list):
			if j < len(V):
				Y[i]=V[j]
			else:Y[i]=None 
		elif isinstance(V, dict):
			if i in V.keys():
				Y[i]=V[i]
			else:Y[i]=None
	return Y
def EQUAL(X):return len(union(X,X)) < 2
def NOT_EQUAL(X):return len(union(X,X)) == len(X)
def ANY_EQUAL(x):return EQUAL(x) or (not EQUAL(x) and not NOT_EQUAL(x))
def TYPE(X):
	x,t = X
	if isinstance(x, list):
		for i in x:
			if not TYPE([i,t]):
				return False
		return True
	else:return isinstance(x,t)
def NOT_TYPE(X):
	x,t = X
	if isinstance(x, list):
		for i in x:
			if TYPE([i,t]):
				return False
		return True
	else:return not isinstance(x,t)
def ANY_TYPE(x):return TYPE(x) or (not TYPE(x) and not NOT_TYPE(x))
def IN(X):
	x,t = X
	if isinstance(x, list):
		for i in x:
			if not IN([i,t]):
				return False
		return True
	else:return x in t
def NOT_IN(X):
	x,t = X
	if isinstance(x, list):
		for i in x:
			if IN([i,t]):
				return False
		return True
	else:return x not in t
def ANY_IN(x):return IN(x) or (not IN(x) and not NOT_IN(x))
def Store(X, i, v):
	X[i] = v
	return X
def Index(X, x):
	if isinstance(X, list):
		return [i for i in range(len(X)) if X[i] == x]
def Execute(f, x):return f(x)
def Remove(X, i):
	del X[i]
	return
def INDEX(X, I):
	Y = []
	if isinstance(I, list):
		for i in I:
			Y.append(Index(X, i))
		return Y
	else:
		return Index(X, I) 
def STORE(X, I, V):
	Y = Matrix(X)
	for j in range(len(I)):
		i = I[j]
		v = V[j]
		Store(Y, i, v)
	return Y
def EXECUTE(*D):
	if isinstance(D, tuple):
		if len(D) == 1:
			if isinstance(D[0], tuple) or isinstance(D[0], list):
				D = D[0]
		if len(D) >= 1:
			f = D[0]
			X = D[1:]
			self(f,X)
			Y = Matrix([])
			if isinstance(X, tuple) or isinstance(X, list):
				for i in range(len(X)):
					if isinstance(X[i], tuple) or isinstance(X[i], list):
						Y.append(Execute(f, (X[i])))
					else:
						Y.append(Execute(f, X[i]))
				return Y
			else:execute(f, X)
def Construct(keys, data=None):
	output = Schema()
	if data == None:
		return
	index = 0
	for i in range(len(keys)):
		key = keys[i]
		value = data[i]
		index = len(output.keys())
		if TYPE([[value, key], list]):
			output[index] = Construct(key, value)
		elif Type([value, type]):
			if isinstance(value, list):
				output[index] = Construct(key, value)
			else:output[key] = value
		else:
			output[key] = value

	return Schema().create(output)

class Data(Dictionary):
	def __init__(self, value=None):
		self['value'] = value
	def __call__(self):
		return self['value']

class Schema(Dictionary):
	def __init__(self):
		super().__init__()

	def create(self, data):
		if isinstance(data, Data):
			return data['value']
		elif isinstance(data, dict):
			for i in data.keys():
				self[i] = Schema().create(data[i])
		elif isinstance(data, list):
			for i in range(len(data)):
				self[i] = Schema().create(data[i])
		elif isinstance(data, tuple):
			return self.create(create_dict(data[0], data[1]))
		else: return data
		return self

	def compile(self, i='values'):
		values = self.retrieve(i)
		if isinstance(values, Schema):
			values = list(values.get_values(values.keys()))
		output = []
		for j in range(len(values)):
			if isinstance(values[j], Schema):
				y = values[j]
				if isinstance(y, Schema):
					y = y.retrieve('values')
			else:y = values[j]
			output.append(y)
		return output

	def retrieve(self, i='keys'):
		if i == 'keys':
			values = self.keys()
		elif i == 'values':
			values = [self[i] for i in self.keys()]
		elif i == 'types':
			values = [type(self[i]) for i in self.keys()]
		leaf = True
		label = i
		keys = self.keys()
		index = 0
		output = Schema()
		for i in keys:
			value = values[index]
			if isinstance(self[i], Schema):
				if leaf == True:leaf = False
				value = self[i].retrieve(label)
			else:
				value = values[index]
			output[i] = value
			index += 1
		if leaf == True:
			return values
		return output

class Template(Dictionary):
	def __init__(self, const_data=[]):
		schema = Schema().create(const_data)
		super().__init__(schema)
		self['const'] = []
		self['def'] = []
		for i in self.keys():
			self.set_const(i)
	def keys(self):return compliment(['const', 'def'], super().keys())
	def set_all(self, *data):
		if len(data) == 2:
			if isinstance(data[0], list) and isinstance(data[1], list):
				if len(data[0]) == len(data[1]):
					for i in range(len(data[0])):
						self[data[0][i]] = data[1][i]
		elif len(data) == 1:
			if isinstance(data[0], list):
				for i in range(len(data[0])):
					self[data[0][i]] = None
		return self
	def create(self, data):return Schema().create(self).create(data)
	def is_const(self, key):return key not in self['const']
	def is_def(self, key, val=None):return key in self['def']
	def set_const(self, key, val=None):
		if key not in self:
			self[key] = val
		elif val != None:
			self[key] = val
		if key not in self['const']:
			self['const'].append(key)
	def set_def(self, key):
		if key not in self['def']:
			self['def'].append(key)

class Composite:
	pass

class Collection(list):
	def tolist(self):
		return list(self)

class Function(Template):
	def __init__(self, *data):
		if len(data) == 3:
			f,x,y = data
			self.set_all(['function', 'input', 'output'], [f,x,y])
		elif len(data) == 2:
			f,g = data
			if isinstance(f, Function) and isinstance(g, Function):
				if g.input() != f.output():
					raise Exception('Incoherent functions ' + str(f.type('output')) + ' and ' + str(g.type('input')))
			self.set_all(['function', 'input', 'output'], [Composite, f, g])
	
	def value(self, key):
		if isinstance(key, str) and key in self.keys():
			if not isinstance(self[key], Function):
				return self[key]
			else:return self[key].value(key)
		return key

	def tree(self):
		if self['function'] == Composite:
			tree = [self['input'].tree(), self['output'].tree()]
		else:
			tree = [self['function'], self['input'], self['output']]
		return tree

	def input(self):
		if isinstance(self['input'], Function):
			return self['input'].output()
		else:return self.type('input')
	
	def output(self):
		return self.type('output')

	def check(self, input):
		if isinstance(input, Collection):
			input = input.tolist()
		if not isinstance(input, list):
			input = [input]
		constraints = self.input()
		print(input, constraints)
		if not isinstance(constraints, list):
			constraints = [constraints]

		if len(input) == len(constraints):
			for i in range(len(input)):
				if callable(constraints[i]):
					if not constraints[i](input[i]):
						return False
				elif isinstance(constraints[i], type):
					if not isinstance(input[i], constraints[i]):
						return False
			return True
		return False
	def confirm(self, output):
		if isinstance(output, Collection):
			output = output.tolist()
		if not isinstance(output, list):
			output = [output]
		constraints = self.output()
		print(output, constraints)
		if not isinstance(constraints, list):
			constraints = [constraints]

		if len(output) == len(constraints):
			for i in range(len(output)):
				if isinstance(constraints[i], type):
					if not isinstance(output[i], constraints[i]):
						return False
				elif callable(constraints[i]):
					if not constraints[i](output[i]):
						return False
			return True
		return False
		# if isinstance(input, list) and isinstance(self.input(), list):
		# 		if len(input) == len(self.input()):
		# 			for i in range(len(input)):
		# 				if isinstance(input[i], self.input()[i]):
		# 					return False
		# 			return True
		# elif isinstance(input, self.input()):
		# 	return True
		# return False

	def compute(self, input):
		if self.type('function') != Composite:
			if self.check(input):
				if isinstance(input, Collection):
					x = input.tolist()
					output = self['function'](*x)
				else:output = self['function'](input)
				if self.confirm(output):
					return output
				else:raise Exception('Invalid output type')
			else:raise Exception('Invalid input type: ' + str(type(input)) + ' (should be ' + str(self.input()) + ')')
		else:
			input = self['input'].compute(input)
			if isinstance(input, self.input()):
				output = self['output'].compute(input)
				if self.confirm(output):
					return output
				else:raise Exception('Invalid output type')
			else:raise Exception('Invalid input type: ' + str(type(input)) + ' (should be ' + str(self.output()) + ')')
			return output
	
	def type(self, key):
		value = self.value(key)
		if isinstance(value, type):
			return value
		return type(value)

def Compose(*data):
	return Function(*data)
def Check(f, *data):
	return f.valid(*data)
def Compute(f, data):
	return f.compute(data)

def f(x):
	return x
def g(x):
	return str(x)
def h(x):
	return int(x)

def f1(x):
	return [f(x), g(x)]
def f2(x):
	return len(x)

def Recursion(X, function):
	if isinstance(X, list):
		Y = []
		for i in range(len(X)):
				Y.append(f())
		return Y
	elif isinstance(X, Function):
		return Retrieve(X.tree(), function)

def MUL(*X):
	x = X[0]
	Y = [x]
	for i in range(1, len(X)):
		x,y = Y[0], X[i]
		# Y[0] = y
		if isinstance(x, list):
			if isinstance(y, list):
				Y[0] = x + y
			else:
				Y[0] = x + [y]
		elif isinstance(y, list):
			Y[0] = [x] + y
		else:
			Y[0] = [x,y]
	return Y[0]

def ADD(*X):
	x = X[0]
	Y = [x]
	for i in range(1, len(X)):
		x,y = Y[0], X[i]

		if isinstance(x, list):
			if isinstance(y, list):
				Y[0] = x + y
			else:
				Y[0] = x + [y]
		elif isinstance(y, list):
			Y[0] = [x] + y
		else:
			Y[0] = [x,y]
	return Y[0]

x = [2], [2, [3]], 2, [2, 3, [4]]
# x = __mul__(*x)
# x = __mul__(*x)
# y = __mul__(*x)
print(x)


def Tree(X):
	return X.tree()

logical_functions = Dictionary({		
	'copy':copy,
	'create_dict':create_dict,
	'EQUAL':EQUAL,
	'NOT_EQUAL':NOT_EQUAL,
	'ANY_EQUAL':ANY_EQUAL,
	'TYPE':TYPE,
	'NOT_TYPE':NOT_TYPE,
	'ANY_TYPE':ANY_TYPE,
	'IN':IN,
	'NOT_IN':NOT_IN,
	'ANY_IN':ANY_IN,
	'Store':Store,
	'Index':Index,
	'Execute':Execute,
	'Remove':Remove,
	'INDEX':INDEX,
	'STORE':STORE,
	'EXECUTE':EXECUTE,
	'Construct':Construct
})

meta_functions = Dictionary({
	'compose':Compose,
	'compute':Compute,
	'check':Check,
	'tree':Tree,
	'recursion':Recursion
})
