from topology import *
from function_language import *
from lib.relations import *

def shuffle(x):
	y = []
	v = list(x)
	done = False
	while not done:
		if len(v) == 0:
			done = True
		else:
			i = rr(len(v))
			y.append(v[i])
			del v[i]
	return y

def reorder(x, k):
	y = []
	for i in range(len(x)):
		y.append(x[k[i]])
	return y

def display(data, indent=''):
	string = ''
	if isinstance(data, dict):
		string = ''
		for i in data.keys():
			x = data[i]
			s = indent + str(i) + ':  '
			if isinstance(x, dict) or isinstance(x, list):
				# ind = indent + '	'
				ind = ' '
				if isinstance(x, dict):
					s += '\n'
					ind = indent + '	'
				s += display(x, ind)
			else:
				s += indent
				s += str(x)
			s += '\n'
			string += s
	elif isinstance(data, list):
		s = []
		for x in data:
			s.append(str(x))
		string = indent + '{' + merge(',', s) + '}'
	if indent == '':
		print(string)
	else:return string

def NULL(*X):
	pass

class FunctionalDictionary(Dictionary):
	def keys(self):
		keys = []
		for i in super().keys():
			if isinstance(i,str) and '.' not in i:
				keys.append(i)
		return keys
	def get_dependent(self, key, ext):
		i = merge('.', [str(key), str(ext)])
		return self[i]
	def set_dependent(self, key, ext, val=None):
		i = merge('.', [str(key), str(ext)])
		self[i] = val

class FunctionalTopology(FunctionalDictionary):
	def __init__(self, inputs, capacity, functions=None, weights=None, thresholds=None):
		for i in range(len(inputs)):
			k = str(i)
			x = inputs[i]
			if x != None:
				x = [x]
				for j in range(len(x)):
					x[j] = str(x[j])

			if functions == None:
				f = None
			else:f = functions[i]
			if weights == None:
				if x != None:
					w = [1 for i in range(len(x))]
				else:w = []
			else:
				w = weights[i]
			
			if thresholds == None:
				t = None
			else:t = thresholds[i]
			self.set_node(k,f,x,w,t)
		self.init(capacity)
	
	def init(self, capacity):
		state = None
		goals = []
		history = []
		schedule = []
		interface = self.set_interface()
		self.set_dependent('', 'state', state)
		self.set_dependent('', 'history', history)
		self.set_dependent('', 'capacity', capacity)
		self.set_dependent('', 'schedule', schedule)
		self.set_dependent('', 'interface', interface)
		self.set_dependent('', 'goals', goals)
		for i in self.keys():
			targets = self.set_targets(i)
			self.set_dependent(i, 'targets', targets)
	
	def set_node(self, key, function=None, inputs=None, weights=None, threshold=None):
		self.set_value(key, unknown)
		self.set_function(key, function)
		self.set_inputs(key, inputs)
		self.set_weights(key,  weights)
		self.set_threshold(key, threshold)
	
	def get_function(self, key):
		return self.get_dependent(key, 'function')
	def set_function(self, key, function):
		self.set_dependent(key, 'function', function)
	def execute_function(self, function, values):
		try:return function(values)
		except:return unknown

	def get_inputs(self, key):
		return self.get_dependent(key, 'inputs')
	def set_inputs(self, key, inputs):
		self.set_dependent(key, 'inputs', inputs)

	def get_weights(self, key):
		return self.get_dependent(key, 'weights')
	def set_weights(self, key, weights):
		self.set_dependent(key, 'weights', weights)
	
	def get_state(self):
		return self.get_dependent('', 'state')
	def set_state(self, state):
		self.set_dependent('', 'state', state)

	def get_capacity(self):
		return self.get_dependent('', 'capacity')
	def set_capacity(self, capacity):
		self.set_dependent('', 'capacity', capacity)

	def get_threshold(self, key):
		return self.get_dependent('', 'threshold')
	def set_threshold(self, key, threshold):
		self.set_dependent(key, 'threshold', threshold)
	
	def get_targets(self, key):
		return self[key + '.targets']
	def set_targets(self, key):
		targets = []
		for i in self.keys():
			inputs = self.get_inputs(i)
			if inputs != None and key in inputs:
				targets.append(i)
		return targets

	def get_goals(self):
		return self.get_dependent('', 'goals')
	def set_goals(self, goals):
		self.set_dependent('', 'goals', goals)
	
	def get_interface(self):
		return self['.interface']
	def set_interface(self):
		roots = self.keys()
		leaves = list()
		for i in self.keys():
			x = self.get_inputs(i)
			if x == None:leaves.append(i)
			else:
				for j in x:
					if j in roots:
						del roots[roots.index(j)]
		return leaves, roots

	def get_history(self):
		return self['.history']
	def set_history(self, key):
		self['.history'].append(key)
		history = self.get_history()
		capacity = self.get_capacity()
		if len(history) > capacity:
			difference = len(history) - capacity
			self['.history'] = history[difference:len(history)]
			for i in range(difference):
				k = history[i]
				self[k] = unknown
	
	def get_schedule(self):
		return self['.schedule']
	def set_schedule(self, key):
		if isinstance(key, list):
			for k in key:self.set_schedule(k)
		else:self['.schedule'].append(key)
	def update_schedule(self, key):
		schedule =  self.get_schedule()
		if key in schedule:
			index = schedule.index(key)
			del schedule[index]

	def get_value(self, key):
		return self[key]
	def set_value(self, key, value):
		self[key] = value
	
	def get_values(self, keys):
		values = []
		for i in keys:
			values.append(self[i])
		return values
	def set_values(self, keys, values):
		j = 0
		for i in range(len(keys)):
			k = keys[i]
			v = values[i]
			self[k] = v

	def get_leaves(self):
		return self.get_interface()[0]
	def get_roots(self):
		return self.get_interface()[1]
	def get_recent(self):
		return self.get_history()[0]

	def inputs(self, values):
		leaves = self.get_leaves()
		self.set_values(leaves, values)
	def outputs(self):
		roots = self.get_roots()
		return self.get_values(roots)	
	def compute(self, key):
		sources = self.get_inputs(key)
		if sources != None:
			inputs = self.get_values(sources)
			if unknown not in inputs:
				function = self.get_function(key)
				output = self.execute_function(function, inputs)
				self.set_history(key)
			else:output = unknown
			self[key] = output
		return self[key]
	
	def select(self, paths):
		options = []
		scores = []
		for i in paths:
			if self[i] == unknown:
				sources = self.get_inputs(i)
				inputs = self.get_values(sources)
				weights = self.get_weights(i)
				score = 0
				for j in range(len(inputs)):
					w = weights[j]
					x = 1
					if w == None: w = 1
					if inputs[j] == unknown: x = -1
					score += x*w * 1/len(inputs)
				scores.append(score)
				options.append(i)
		indices = sort(options)
		options = reorder(options, indices)
		return options

	def update(self):
		schedule = self.get_schedule()
		if len(schedule) > 0:
			done = False
			while not done:
				if len(schedule) == 0:
					done = True
				else:
					current = schedule[0]
					if current != None:
						self.compute(current)
						self.set_state(current)
						done = True
					self.update_schedule(current)
		else:
			history = self.get_history()
			if len(history) > 0 and history[len(history)-1] != None:
				recent = self.get_recent()
				if recent != None:
					targets = self.get_targets(recent)
					if targets != None:
						selection = self.select(targets)
						self.set_schedule(selection)
			else:
				leaves = self.get_leaves()
				targets = list()
				for i in leaves:
					targets = union(targets, self.get_targets(i))
				if targets != None:
					selection = self.select(targets)
					self.set_schedule(selection)

	def describe(self):
		roots = self.get_roots()
		outputs = self.get_values(roots)
		history = self.get_history()
		schedule = self.get_schedule()
		return [history, schedule, outputs]
		# description = Dictionary({'history':history, , 'schedule':schedule})
