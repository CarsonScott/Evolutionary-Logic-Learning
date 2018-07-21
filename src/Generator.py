from lib.util import * 
from lib.relations import *
def is_type(x, t):
	if isinstance(t, type):
		return isinstance(x, t)
	elif isinstance(t, str):
		return get_name(x) == t
	else: 
		return is_type(x, get_name(t))
def get_name(x):
	try:return str(x.__name__).lower()
	except:return str(type(x).__name__).lower()

def get_class(x):
	return str(x.__class__)

def has_name(x, n):
	return get_name(x) == n

def get_value(M, i):
	return M.get_value(i)

def is_value(x):
	return x != None

def is_function(f):
	return callable(f)

def call_function(f):
	return f()

def has_element(X, i):
	if is_type(X, list):
		if is_type(i, int) and i < len(X) and i >= 0:
			return True
	elif is_type(X, Memory):
		if i in X.get_keys():
			return True
	elif is_type(X, Dict):
		if i in X.keys():
			return True
	return False

def is_equal(x, y):
	return x == y

def all_true(X):
	for x in X:
		if not x:
			return False
	return True

def some_true(X):
	for x in X:
		if x:
			return True
	return False

class Memory(list):
	def __init__(self):
		self.indices = Dict()
	def get_index(self, key):
		return self.indices[key]
	def get_value(self, index):
		return super().__getitem__(index)
	def get_keys(self):
		return self.indices.keys()
	def get_size(self):
		return len(self.indices)
	def has_element(self, key):
		return has_element(self, key) or has_element(self.indices, key)

	def __getitem__(self, key):
		if self.has_element(key):
			index = self.get_index(key)
			return self.get_value(index)
	def __setitem__(self, key, value):
		if self.has_element(key):
			index = self.get_index(key)
			super().__setitem__(index, value)
		else:
			self.append(value)
			index = len(self)-1
			self.indices[key] = index

	def convert(self):
		output = Dict()
		for i in self.get_keys():
			output[i] = self[i]
		return output

class Generator(Memory):
	def __init__(self, size):
		# self.function = compute
		self.capacity = size
		self.history = [None for i in range(size)]
		self.input = None
		self.output = None
		self.current = None
		self.iteration = 0
		self.state = 0

	def __call__(self, data):
		self.input = data
		self.update()
		self.store()
		self.compute()
		self.iteration += 1
		return self.output

	def update(self, input):
		if is_type(self.current, Generator):
			self.state = 1
		else:self.state = 0

		if self.input == ' ' or len(self.history) == 0:
			self.history.append(Generator(0))
			output = self.history
		elif self.input == ';':
			output = self.history
			self.history = []
		else:
			self.history[len(self.history)-1].update(self.input)
			output = self.history
		return output
		


	def store(self):
		if self.state == 1:
			self.input = self.current(self.input)
			if self.input != None:
				self.current = self.input
		else:
			if self.input == 'create':
				self.current = Generator(4, f1)
				self.input = None

		if self.input != None:
			self.current = self.input
			self.history.insert(0, self.current)
			del self.history[self.capacity]

	def compute(self):
		self.output = self.function(self)
		if self.output != None:
			self.current = self.output

def f1(generator):
	if all_equal(to_set(get_size(generator.history), generator.capacity)):
		names = to_all(generator.history, get_name)
		types = union(names, names)

		output = Memory()
		for i in types:
			if i != 'nonetype':
				output[i] = []
		for i in range(len(names)):
			y = generator.history[i]
			if y != None:
				output[names[i]].append(y)
		return output.convert()

class GET:
	def __init__(self, key):
		self.key = key
	def __call__(self, inputs):
		return inputs[self.key]

def difference(inputs):
	outputs = []
	for i in range(1, len(inputs)):
		outputs.append(inputs[i]-inputs[i-1])
	return outputs

def get_keys(inputs):
	if is_type(inputs, Dict):
		return inputs.keys()
	elif is_type(inputs, Memory):
		return inputs.get_keys()

def to_set(*all):
	outputs = []
	for x in all:
		outputs.append(x)
	return outputs

def all_equal(inputs):
	p = inputs[0]
	for x in inputs:
		if x != p:
			return False
		p = x
	return True

def get_size(inputs):
	return len(inputs)

def appy_to(function, input):
	return function(input)

def to_all(inputs, function):
		outputs = []
		for x in inputs:
			outputs.append(function(x))
		return outputs

def all_to(input, functions):
	outputs = []
	for f in functions:
		outputs.append(f(input))
	return outputs


g = Generator(0)


X = 'a and b; c and d;'
for i in range(len(X)):
	print(g.update(X[i]))
print(g.update(''))
