from topology import *
from settheory import *

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

class FunctionalTopology(Dictionary):
	def __init__(self, inputs, history_size, schedule_size, functions=None, weights=None, thresholds=None):
		for i in range(len(inputs)):
			k = str(i)
			x = inputs[i]
			if functions == None:
				s = None
			else:s = functions[i]
			if weights == None:
				w = [1 for j in inputs]
			else: w = weights[i]
			if thresholds == None:
				t = None
			else:t = thresholds[i]
			self.set(k,s,x,w,t)
		self.init(history_size, schedule_size)
			
	def keys(self):
		keys = []
		for i in super().keys():
			if isinstance(i,str) and '.' not in i:
				keys.append(i)
		return keys

	def get_values(self, keys):
		values = []
		for i in keys:
			values.append(self[i])
		return values

	def init(self, history_size, schedule_size):
		history = [None for i in range(history_size)]
		self.set_dependent('', 'history', history)
		schedule = []
		self.set_dependent('', 'schedule', schedule)
		interface = self.compute_interface()
		self.set_dependent('', 'interface', interface)
		for i in self.keys():
			targets = self.compute_targets(i)
			self.set_dependent(i, 'targets', targets)
	def set(self, key, function=None, inputs=None, weights=None, threshold=None):
		self[key] = unknown
		self.set_function(key, function)
		self.set_inputs(key, inputs)
		self.set_weights(key,  weights)
		self.set_threshold(key, threshold)
	def set_dependent(self, key, ext, val=None):
		i = merge('.', [str(key), str(ext)])
		self[i] = val
	def set_function(self, key, function):
		self.set_dependent(key, 'function', function)
	def set_inputs(self, key, inputs):
		self.set_dependent(key, 'inputs', inputs)
	def set_weights(self, key, weights):
		self.set_dependent(key, 'weights', weights)
	def set_threshold(self, key, threshold):
		self.set_dependent(key, 'threshold', threshold)
	def get_function(self, key):
		return self[key + '.function']
	def get_inputs(self, key):
		return self[key + '.inputs']
	def get_weights(self, key):
		return self[key + '.weights']
	def get_threshold(self, key):
		return self[key + '.threshold']
	def get_targets(self, key):
		return self[key + '.targets']
	def get_interface(self):
		return self['.interface']
	def get_history(self):
		return self['.history']
	def get_schedule(self):
		return self['.schedule']
	def compute_interface(self):
		roots = self.keys()
		leaves = list()
		for i in self.keys():
			x = self.get_inputs(i)
			if x == None:
				leaves.append(i)
			else:
				for j in x:
					if j in roots:
						del roots[roots.index(j)]
		return leaves, roots
	def compute_targets(self, key):
		targets = []
		for i in self.keys():
			inputs = self.get_inputs(i)
			if inputs != None and key in inputs:
				targets.append(i)
		return targets

	def set_values(self, keys, values):
		j = 0
		for i in keys:
			self[i] = values[j]
			j += 1 

	def update_leaves(self, values):
		inputs = self.get_interface()[0]
		self.set_values(inputs, values)
	def update_history(self, key):
		self['.history'].append(key)
		old = self['.history'][0]
		del self['.history'][0]
		self[old] = unknown

	def set_schedule(self, key):
		if isinstance(key, list):
			for k in key:self.set_schedule(k)
		else:self['.schedule'].append(key)
	def del_schedule(self, key):
		del self['.schedule'][self['.schedule'].index(key)]

	def execute(self, function, values):
		try:
			return function(values)
		except:return unknown

	def compute(self, key):
		sources = self.get_inputs(key)
		if sources != None:
			inputs = self.get_values(sources)
			if unknown not in inputs:
				function = self.get_function(key)
				output = self.execute(function, inputs)
				self.update_history(key)
			else:output = unknown
			self[key] = output
		return self[key]

	def select(self, targets):
		options = []
		scores = []
		for i in targets:
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

	def __call__(self):
		current = None
		schedule = self.get_schedule()
		if len(schedule) > 0:
			done = False
			while not done:
				if len(schedule) == 0:
					done = True
				else:
					current = schedule[0]
					if current != None:
						done = True
						self.compute(current)
					self.del_schedule(current)
		else:
			history = self.get_history()
			if len(history) > 0 and history[len(history)-1] != None:
				recent = history[len(history)-1]
				if recent != None:
					targets = self.get_targets(recent)
					if targets != None:
						selection = self.select(targets)
						self.set_schedule(selection)
			else:
				leaves = self.get_interface()[0]
				targets = list()
				for i in leaves:
					targets = union(targets, self.get_targets(i))
				if targets != None:
					selection = self.select(targets)
					self.set_schedule(selection)

		roots = self.get_interface()[1]
		outputs = self.get_values(roots)
		if unknown not in outputs:
			return outputs