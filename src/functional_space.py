from matrix import *
from dictionary import *
from lib.relations import *
from functional_logic import *
import os

def Union(*X):
	x = X[0]
	for i in range(1, len(X)):
		x = union(x, X[i])
	return x
def Intersection(*X):
	x = X[0]
	for i in range(1, len(X)):
		x = intersection(x, X[i])
	return x
def Equivalent(*X):
	x = X[0]
	for i in range(1, len(X)):
		if not equivalent(x, X[i]):
			return False
	return True

def identity(x):
	return x

class Group(Dictionary):
	def __init__(self, *X):
		K = [x.keys() for x in X]
		if Equivalent(*K):
			self.members = X
			for i in Union(*K):
				self[i] = identity
		else:raise Exception('incompatible group ' + str(X))
	def assign(self, key, function):
		self[key] = function
	def update(self, key):
		function = self[key]
		inputs = [x[key] for x in self.members]
		return function(inputs)
	def __call__(self):
		output = Dictionary()
		for i in self.keys():
			output[i] = self.update(i)
		return output

KEYS = 'keyspace'
VALUES = 'valuespace'

class Null:
	pass

def valid(f, x):
	try:
		f(x)
	except:
		return False
	return True

def apply(f, X):
	return [f(x) for x in X]

def equal(X):
	x = X[0]
	for i in range(len(X)):
		if x != X[i]:
			return False
		x = X[i]
	return x

def true(X):
	return equal(apply(type, X)) and X[0] == True

def concatenate(*X):
	x = []

	for i in range(len(X)):
		v = X[i]
		if not isinstance(v, list):
			if isinstance(v, tuple):
				v = list(v)
			else:v = [v]
		x += v
	return x

def pushdown(X, I):
	Y = []
	G = []
	for i in range(len(X)):
		if i in I:
			G.append(X[i])
		else:Y.append(X[i])
	Y.append(G)
	return Y

def popup(X, i):
	Y = []
	for j in range(len(X)):
		if j == i:
			Y += X[j]
		else:
			Y.append(X[j])
	return Y

x = pushdown('a b c d e f g h'.split(), [0, 1, 4])
y = popup(x, len(x)-1)
print(x)
print(y)

class Universe(Dictionary):
	def __init__(self, *data):
		super().__init__(*data)
		self.local_memory = []
	def __getitem__(self, key):
		if key == KEYS:
			return self.keys()
		if key == VALUES:
			return self.values()
		return super().__getitem__(key)
	def set(self, key, value):
		self[key] = value
	def get(self, key):
		return self[key]
	def rem(self, key):
		del self[key]
	def retrieve(self, space, element):
		return self[space][element]
	def append(self, space, element):
		self[name].append(element)
	def remove(self, space, element):
		del self[space][element]
	def group(self, key, elements):
		self[key] = Universe()
		for i in elements:
			self[key][i] = self[i]
		return self[key]
	def transform(self, source, function, target):
		space = Universe()
		for i in self[source].keys():
			space[i] = function(self[source][i])
		self[target] = space
		return space
	
	def convert(self, data):
		if isinstance(data, Dictionary):
			keys = data.keys()
			if contains(keys, ['function', 'input']):
				f = data['function']
				v = data['input']
				if isinstance(v, tuple):
					y = f(*v)
				else:y = f(v)
				return y
		return data
	
	def compute(self, data):
		if isinstance(data, Dictionary):
			y = Dictionary()
			vals = []
			for i in data.keys():
				vals.append(data[i])
				y[i] = self.compute(data[i])
			if len(data) > 1:
				self.local_memory = union(self.local_memory, data)
			return y
		elif isinstance(data, list):
			y = []
			for i in range(len(data)):
				y.append(self.compute(data[i]))
			if len(data) > 1:
				self.local_memory = union(self.local_memory, data)
			return y
		if data in self.keys():
			return self[data]
		return data

def Keys(X):
	return X.keys()
def Transform(X, *data):
	return X.transform(*data)
def Group(X, *data):
	return X.group(*data)
def Equal(*data):
	for i in range(len(data)-1):
		X = data[i]
		Y = data[i+1]
		if type(X) != type(Y):
			return False
		if isinstance(X, Dictionary):
			if not equivalent(X.keys(), Y.keys()):
				return False
			for i in X.keys():			
				if not Equal(X[i],Y[i]):
					print(X[i], Y[i])
					return False
			# return True
		elif isinstance(X, list):
			if len(X) != len(Y):
				return False
			for i in range(len(X)):
				if not Equal(X[i], Y[i]):
					return False
			# return True
		else:
			if X != Y:
				return False
	return True

def Apply(f, X):
	if isinstance(X, Dictionary):
		Y = Dictionary()
		for i in X.keys():
			Y[i] = Apply(f, X[i])
		return Y
	if isinstance(X, list):
		Y = []
		for i in range(len(X)):
			Y.append(Apply(f, X[i]))
		return Y
	if isinstance(f, Dictionary):
		Y = Dictionary()
		for i in f.keys():
			print(f[i])
			Y[i] = Apply(f[i], X)
		return Y
	if isinstance(f, list):
		Y = []
		for i in range(len(f)):
			Y.append(Apply(f[i], X))
		return Y
	if callable(f):	
		return f(X)
def Transpose(X):
	if isinstance(X, list):
		if Equal(*Apply(type, X)):
			if isinstance(X[0], Dictionary):
				Y = Dictionary()
				for i in X[0].keys():
					Y[i] = []
					for j in range(len(X)):
						Y[i].append(Transpose(X[j][i]))
				return Y
	else:return X

x = Dictionary({'x':1, 'y':2})
y = Dictionary({'x':0, 'y':3})
z = Dictionary({'x':x, 'y':y})
U = Universe()

U.set('X', x)
U.set('Y', y)
U.set('Z', z)

for i in range(10):
	U[i] = i

y = U.compute([[0, [1, [1, 2]]], [[3, 4]]])
print(U.local_memory)

universe = Universe()
universe.set('a', Universe({'x':1,'y':2}))
universe.set('b', Universe({'x':1,'y':2}))
universe.set('c', Universe({'x':1,'y':2}))
universe.set('d', Universe({'x':1,'y':2}))
#print(universe)
#print(universe.group('e', ['a', 'b']))
#print(universe.transform('f', Keys, 'e'))

# # print(concatenate('a', 'b', 'c'))
# # print(universe)
# # print(universe.retrieve('a', 'x'))

# g = Group(Dictionary({'a':1, 'b':1}), Dictionary({'a':3, 'b':5}))
# g.assign('a', sum)
# g.assign('b', sum)
# print(g())

# help(os)

def norm(x):
	if abs(x) > 1:
		x = x/abs(x)
	return x

def ratio(x):
	return min(x) / max(x)
	y = []
	for i in x:
		y.append(i*r)
	return y

def distance(a, b):
	if type(a) == type(b):
		if type(a) in [Matrix, list]:
			# r = ratio([abs(a[i]-b[i]) for i in range(len(a))])
			if len(a) == len(b):
				y = 0
				for i in range(len(a)):
					o = distance(a[i], b[i])
					print(o)
					y += o * 1/len(a)
				# 	if isinstance(a, Matrix):
				# 	elif isinstance(a, list):
				# 		y += a[i] - b[i]
				return y / len(a)
	y = 0 
	x = [a,b]
	r = ratio(x)
	print(r)
	for i in range(1, len(x)):
		d = a-b
		y += pow(d, 2) * 1/len(a)
	return y
		# if isinstance(a, list):
		# print(a,r)
		# 	return 
		# elif type(a) in [float, int]:
# 		# 	a,b = ratio([a,b])

# print(distance(Matrix([2,[3,4]]), Matrix([2,[3,3]])))
# print(distance([2,3,5]))
# print(distance([2,4], [2,3]))
# # print(distance(4,3))

input()