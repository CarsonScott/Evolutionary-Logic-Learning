from pattern_memory import *
from old.histogram import *
from old.stream import *
import random
import os
from lib.relations import *
from lib.data import *
random.seed()

def index(*data):
	X = list(data)
	y = ''
	for x in X:
		y += str(x) + ','
	return y[:len(y)-1]

class EquationMemory(PatternMemory):
	def initialize(self):
		self['+'] = add
		self['tanh'] = tanh
		self['softmax'] = softmax
		self['logistic'] = logistic
		self['+'] = add
		self['+'] = add
		self['-'] = sub
		self['*'] = mul
		self['/'] = div
		self['^'] = Pow
		self['>'] = gt
		self['<'] = lt
		self['='] = eq
		self['!='] = neq
		self['>='] = gteq
		self['<='] = lteq
		self['&'] = And
		self['!'] = Not
		self['|'] = Or

	def load(self, folder):
		directory = os.listdir(folder)

		for i in directory:
			file = i
			data = load(folder + '/' + file)
			self.set_object(i, data)

	def __init__(self, size, buffer):
		super().__init__()
		self.initialize()
		self.size = size
		self.buffer = buffer
		self.states = Dict()
		self.averages = Dict()
		self.logs = Dict()
		self.sizes = Dict()
		self.roots = list()
		self.worlds = Dict()
		self.scores = Dict()
		self.levels = Dict()
		self.updated = list()
		self.structures = Dict()
		self.outputs = Dict()
		self.inputs = list()
		self.utilities = Dict()
		self.dependents = Dict()
		self.dependencies = Dict()
		self.functions = list()
		self.variables = list()
		self.classes = Dict({'operation': ['+', '-', '*', '/', '^', 'tanh', 'softmax', 'logistic'],
							 'proposition': ['>', '<', '=', '!=', '>=', '<=', '&', '|', '!']})

	# def collect_functions(self):
	# 	for i in self.outputs.keys():

	# 		self.identify(self[i]) == 'op':

	# 		self.identify(self[i]) == 'pattern':

	# 		self.identify(self[i]) == 'data':
	
	def get_parameters(self, key):
		if key in self.outputs.keys():
			key = self[key][0]
		if key in self.outputs.keys():
			return signature(self[key]).parameters

	def classify(self, key):
		for c in self.classes.keys():
			if key in self.classes[c]:
				return c

	def set_object(self, key, value, input=True):
		self[key] = value
		self.averages[key] = Histogram(100)
		self.logs[key] = Stream(self.buffer)
		self.outputs[key] = value
		if input:self.inputs.append(key)
		self.dependencies[key] = []
		self.dependents[key] = []
		self.utilities[key] = 0
		self.states[key] = None
		self.structures[key] = None

	def del_object(self, key):
		del self[key] 
		del self.structures[key]
		del self.averages[key]
		del self.logs[key]
		del self.outputs[key] 
		if key in self.inputs:
			del self.inputs[self.inputs.index(key)]
		del self.dependencies[key]
		del self.dependents[key]
		del self.utilities[key]

	def set_world(self, world, size=None):
		self.worlds[world] = []
		self.scores[world] = 0
		self.sizes[world] = size

	def compute_score(self, world):
		data = self.worlds[world]
		size = self.sizes[world]
		lower_bounds, upper_bounds = self.bounds[world]
		lower_limit, upper_limit = self.limits[world]
		score = logistic(size - lower_bounds) + logistic(upper_bounds - size)
		return score

	def update_scores(self):
		for i in self.worlds.keys():
			world = self.worlds[world]
			score = self.compute_score(world)
			self.scores[world] = score

	def update_log(self, key):
		y = self.outputs[key]
		a = self.averages[key].update(y)
		self.logs[key].add(self.outputs[key])

	def update_inputs(self, data):
		for i in range(len(data)):
			key = self.inputs[i]
			value = data[i]
			self[key] = value

#####################################################################			


	def get_dependencies(self, key):
		if key not in self.updated:
			self.dependencies[key] = []
			self.dependents[key] = []
			variable = self.outputs[key]
			function = variable[0]
			inputs = list(variable[1:])
			if self.identify(variable) == 'pattern':
				for x in inputs:
					y = []
					if x in self.outputs.keys():
						if x not in self.updated:
							self.dependencies[x] = []
							self.dependencies[key].append(x)
						elif key not in self.dependents[x]:
							self.dependents[x].append(key)
						y = self.get_dependencies(x)
						
						self.dependencies[key] += y

				try:
					self[key] = self.compute(tuple([function] + inputs))
				except:
					self[key] = None
			self.updated.append(key)

		return self.dependencies[key]


			# 		self.dependencies[key] = union(self.dependencies[key], self.dependencies[x])
			# 			self.dependents[x] = []
			# 		self.dependents[x] += [key]
		
			# self.dependencies[key] = s
			# 		if self.identify(self[x]) == 'pattern':
			# 			if x not in self.updated:
			# 				self.dependents[x] = [key]
			# 				print(self.get_dependencies(x, False))
			# 			else:self.dependents[x].append(key)


	def update_outputs(self, inputs):
		c = 0
		keys = self.inputs
		for i in range(len(inputs)):
			x = inputs[i]
			self.outputs[c] = x
			c +=1 
		self.updated = self.inputs
		for i in self.outputs.keys():
			if i not in self.updated:
				self.get_dependencies(i)

		if len(self.outputs.keys()) < self.size:
			n = int(1/2*pow(len(self.outputs), 2))
			if n != 0 and rr(int(n)) < len(self.outputs):
				new_object = self.mutate()
				if new_object != None:
					key = random_str(3)
					self.set_object(key, new_object, False)
		elif len(self.outputs.keys()) >= self.size:
			n = int(1/2*pow(len(self.outputs), 2))
			if n != 0 and rr(int(n)) < len(self.outputs):
				options = self.outputs.keys()
				key = rr(len(options))
				key = self.outputs.keys()[key]
				if key not in self.inputs:
					self.del_object(key)
		return self.outputs

	def mutate(self):
		
		roots = self.outputs.keys()
		options = [math.e, math.pi] + [rr(-10, 10) for i in range(10)] + roots
		y = None
		f = None
		X = []

		ofunctions = self.classes['operation']
		pfunctions = self.classes['proposition']
		functions = ofunctions + pfunctions
		
		# if rr(100) == 0:
		# 	if rr(2) == 0:functions = ofunctions
		# 	else:functions = pfunctions

		# random selection
		if rr(2) == 0:
			# input copy
			C = self.translate(roots[rr(len(roots))])
			if self.identify(C) == 'pattern':
				f = C[0]
				X = list(C[1:])
		else:
			# random input
			f = functions[rr(len(functions))]
			X = [options[rr(len(options))] for i in range(rr(2, 4))]

		if len(X) > 0:
			if rr(10) == 0:
				# replacement mutation
				X[rr(len(X))] = options[rr(len(options))]
			if rr(10) == 0:
				# position mutation
				j = rr(len(X))
				k = rr(len(X))
				Xj = X[j]
				Xk = X[k]
				X[j] = Xk
				X[k] = Xj
				
			if rr(10) == 0:
				# insertion mutation
				X.insert(rr(len(X)), options[rr(len(options))])
			# deletion mutation
			if rr(10) == 0:
				del X[rr(len(X))]

		if f == None:
			f = functions[rr(len(functions))]
		y = tuple([f] + X)

		print(y)
		return y


		# options[rr(len(options))]
		# f = None
		# x1 = None
		# X = []
		# if rr(2) == 0:
		# 	# if rr(2) == 0:operators = self.classes['operation']
		# 	# else:operators = self.classes['proposition']
		# 	operators = self.classes['operation']
		# 	f = operators[rr(len(operators))]

		# 	x1 = roots[rr(len(roots))]
		# 	x2 = roots[rr(len(roots))]

		# else:
		# 	O = self.outputs.keys()[self.outputs.keys().index(roots[rr(len(roots))])]
		# 	if self.identify(O) == 'pattern':
		# 		f = O[0]
		# 		X = O[1:]

		# 	if rr(2) == 0:
		# 		X[rr(len(X))] = roots[rr(len(roots))]
		# 			# else:
		# 	else:
		# 		if rr(2) == 0:x1 = O
		# 		else:x2 = O
		# y = (f, x1, x2)
		# return y

	def compress(self, key):
		output = key
		if key in self.outputs.keys(): 
			pattern = self[key]
			output =  pattern
			if self.identify(pattern) == 'pattern':
				function = pattern[0]
				variables = list(pattern[1:])
				for i in range(len(variables)):
					x = variables[i]
					x = self.compress(x)
					variables[i] = x
				output = [function] + variables
		return output

	def extract(self, key):
		pattern = self.compress(key)
		self.del_object(key)
		return pattern

	def score(self, key):
		if output == None:
			score = -1

memory = EquationMemory(100, 20)
memory.load('genetic code')

options =  [True,False] + [i for i in range(-10, 10)] + [math.e, math.pi]
for i in range(19):
	ss = options + memory.outputs.keys()
	key = random_str(4)
	print(key)
	memory.set_object(key, ss[rr(len(ss))], True)

samples = []
for sample in range(20):
	samples.append([])
	for i in range(len(memory.outputs)):
		samples[sample].append([logistic(rr(-10, 10))])

log = open('log.txt', 'w')
index = 0
counter = 0
data = Dict()
for i in range(10000):
	inputs = samples[index]
	index += 1
	if index >= len(samples): 
		index = 0
		counter += 1
	outputs = memory.update_outputs(inputs)
	if i % 100 == 0:
		population = []
		for j in range(10):
			population.append(memory[memory.keys()[rr(len(memory.keys()))]])
		save('genetic code/'+random_str(5), population)

	for i in outputs.keys():
		print(i, outputs[i])
	if counter % 10 == 0:
		string = ''
		logs = memory.logs
		for j in range(memory.buffer):
			string = str(j) + '	'
			for k in logs.keys():
				if len(logs[k]) <= j:
					x = ''
				else:
					x = logs[k][j]
					if identify(x) == 'bool':
						x = int(x)
					x = memory[k]
				string += str(x) + '	'
			print(string)
			log.write(string + '\n')
log.close()