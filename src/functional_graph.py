from dictionary import *
from lib.relations import *
class Trial:
	def __init__(self, event_functions):
		self.functions = event_functions
		self.outputs = [None for i in self.functions]
	def __call__(self, input_data):
		for i in range(len(self.functions)):
			self.outputs[i] = self.functions[i](input_data)
		return self.outputs

def TRUE(x):
	return x is True
def FALSE(x):
	return x is False
def EITHER(x):
	return True
def NEITHER(x):
	return False

def XOR(X):
	return sum(X) == 1
def OR(X):
	return sum(X) > 0
def AND(X):
	return sum(X) == len(X)
def NOT(X):
	return sum(X) == 0
def SUM(X):
	return sum(X)
def AVG(X):
	if len(X) > 0:
		return sum(X) / len(X)
	return 0

def get_true(X):
	Y = []
	for i in range(len(X)):
		if X[i] == True:
			Y.append(i)
	return Y

# trial1 = Trial([TRUE, FALSE])
trial = Trial([XOR, OR, AND, NOT])
labels = ['xor', 'or', 'and', 'not']

Y = []
for i in range(100):
	x = [bool(rr(2)) for i in range(5)]
	y = trial(x)
	print(y)
	Y.append(y)

data = []
prob = []
for i in range(len(Y)):
	indices = get_true(Y[i])
	L = [labels[i] for i in indices]
	if L not in data:
		data.append(L)
		prob.append(1)
	else:
		index = data.index(L)
		prob[index] += 1

for i in range(len(prob)):
	prob[i] /= len(Y)

print(data)
print(prob)

def factorial(n):
	if n <= 1:return 1
	return factorial(n-1)*(n-1)

print(factorial(1))

def identity(x):
	return x

def summation(x):
	y = 0
	for i in x:
		v = 0
		if i != None:
			v = i
		y += v
	return y

class FunctionGraph(Dictionary):

	def __init__(self, history_size=None):
		self.functions = Dictionary()
		self.signatures = Dictionary()
		self.inputs = Dictionary()
		self.outputs = Dictionary()
		self.schedule = list()
		self.interface = list()
		self.history = list()

		self.history_size = history_size

	def get_interface(self):
		return self.interface

	def set_interface(self, inputs, outputs):
		self.interface = (inputs, outputs)

	def get_function(self, key):
		return self.functions[key]
	def set_function(self, key, function):
		self.functions[key] = function

	def get_signature(self, key):
		return self.signatures[key]
	def set_signature(self, key, signature):
		self.signatures[key] = signature

	def get_inputs(self, key):
		return self.inputs[key]
	def set_inputs(self, key, inputs):
		self.inputs[key] = inputs

	def get_outputs(self, key):
		return self.outputs[key]

	def set_outputs(self, key, outputs):
		self.outputs[key] = outputs

	def update_inputs(self, key, inputs=None):
		xsize, ysize = self.get_signature(key)
		if inputs == None:inputs = [None for i in range(xsize)]
		elif not isinstance(inputs, list):inputs = [inputs]
		self.set_inputs(key, inputs)

	def update_outputs(self, key):
		xsize, ysize = self.get_signature(key)
		x = self.get_inputs(key)
		y = self.execute_function(key, x)
		if not isinstance(y, list):
			y = [y for i in range(ysize)]
		for i in range(len(self.outputs[key])):
			x = None
			if i < len(y):x = y[i]
			self.outputs[key][i] = x
		self.set_outputs(key, y)

	def update(self, key, inputs=None):
		self.update_inputs(key, inputs)
		self.update_outputs(key)

	def create(self, key, function, input_size=1, output_size=1):
		if key not in self.keys():self[key] = Dictionary()
		self.set_function(key, function)
		signature = (input_size, output_size)
		self.set_signature(key, signature)
		inputs = [None for i in range(input_size)]
		self.set_inputs(key, inputs)
		outputs = [None for i in range(output_size)]
		self.set_outputs(key, outputs)

	def reset(self, key):
		xsize, ysize = self.get_signature(key)
		inputs = [None for i in range(xsize)]
		self.set_inputs(key, inputs)

	def connect(self, src_key, src_index, dst_key, dst_index):
		if src_key not in self.keys():
			self[src_key] = Dictionary()
		if dst_key not in self[src_key].keys():
			self[src_key][dst_key] = []
		if len(self.outputs[src_key]) > src_index:
			if len(self.inputs[dst_key]) > dst_index:
				value = (src_index, dst_index)
				self[src_key][dst_key].append(value)
			else:raise Exception('Destination index out of range')
		else:raise Exception('Source index out of range')

	def execute_function(self, key, inputs):
		function = self.get_function(key)
		return function(inputs)

	def compute(self, key, inputs):
		if key in self.schedule:
			index = self.schedule.index(key)
			self.schedule.pop(index)
		self.update(key, inputs)
		self.history.append(key)
		if self.history_size != None:
			if len(self.history) > self.history_size:
				error = len(self.history) - self.history_size
				if error > 0:
					removed = self.history[0:error]
					history = self.history[error:len(self.history)]
					self.history = history
					for i in removed:
						self.reset(i)

	def call(self, key=None, inputs=None):
		if key == None:
			if len(self.schedule) > 0:
				key = self.schedule[0]
			else:return

		if inputs != None:
			self.update(key, inputs)
		else:inputs = self.get_inputs(key)
		self.compute(key, inputs)

		links = self[key]
		for dst in links.keys():
			link = links[dst]
			if dst in self.schedule:
				index = self.schedule.index(dst)
				if index > 0:
					val = self.schedule[index-1]
					self.schedule[index-1] = dst
					self.schedule[index] = val
			else:self.schedule.append(dst)

			for c in link:
				i,j = c
				if i < len(self.outputs[key]):
					x = self.outputs[key][i]
					if j < len(self.inputs[dst]):
						self.inputs[dst][j] = x

	def __call__(self, inputs=[]):
		xkeys, ykeys = self.get_interface()
		if  isinstance(inputs, list):
			for i in range(len(inputs)):
				key = xkeys[i]
				self.call(key, inputs[i])

		outputs = list()
		keys = union(reverse(self.schedule), compliment(xkeys, self.keys()))
		for i in keys:
			if i not in xkeys:
				self.call(i)
			if i in ykeys:
				y = self.get_outputs(i)
				if len(y) == 1:
					y = y[0]
				outputs.append(y)
		return outputs

def random_graph_system(keys, history_size=None):
	system = FunctionGraph(history_size)
	for i in keys:
		input_size = rr(1, 4)
		output_size = 1
		function = identity
		if input_size > 1:
			function = summation
		system.create(i, function, input_size, output_size)


	xsize = rr(1, 5)
	prev = [keys[i] for i in range(xsize)]
	keys = compliment(prev, keys)

	while len(keys) > 0:
		dst = keys[rr(len(keys))]
		for k in range(3):
			src = prev[rr(len(prev))]

			src_sig = system.get_signature(src)
			dst_sig = system.get_signature(dst)

			i = rr(src_sig[1])
			j = rr(dst_sig[0])
			system.connect(src, i, dst, j)

		prev.append(dst)
		keys.pop(keys.index(dst))

	return system

keys = [str(i) for i in range(100)]
system = random_graph_system(keys)

system.create('x1', identity, 1, 1)
system.create('x2', identity, 1, 1)
system.create('x3', identity, 1, 1)
system.create('x4', identity, 1, 1)
system.create('x5', identity, 1, 1)
system.create('y1', identity, 1, 1)
system.create('y2', identity, 1, 1)
system.create('y3', identity, 1, 1)
system.set_interface('x1 x2 x3 x4 x5'.split(), 'y1 y2 y3'.split())

inputs, outputs = system.get_interface()

for i in inputs:
	for j in range(3):
		dst = system.keys()[rr(len(system.keys()))]
		system.connect(i, rr(system.get_signature(i)[1]), dst, rr(system.get_signature(dst)[0]))
for i in outputs:
	for j in range(3):
		src = system.keys()[rr(len(system.keys()))]
		system.connect(src, rr(system.get_signature(src)[1]), i, rr(system.get_signature(i)[0]))

x = [1, 1, 1, 1, 1]
for i in range(100):
	if i % 3 == 0:
		y = system(x)
	else:
		y = system()
	for j in range(len(y)):
		if y[j] == None:
			y[j] = 0
	string = ''
	for j in range(len(y)):
		string += str(y[j]) + '	'
	print(str(i) + '	' + string)
