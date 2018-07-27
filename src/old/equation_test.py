from pattern_memory import *

def index(*data):
	X = list(data)
	y = ''
	for x in X:
		y += str(x) + ','
	return y[:len(y)-1]

def random_str(size):
	x = list('abcdefghijklmnopqrstuvwxyz')
	y = ''
	done = False
	while not done:
		c = x[rr(len(x))]
		del x[x.index(c)]
		y += c
		if len(y) == size or len(x) == 0:
			done = True
	return y

class EquationMemory(PatternMemory):
	def __init__(self):
		super().__init__()
		self['store'] = self.__setitem__
		self['+'] = add
		self['-'] = sub
		self['*'] = mul
		self['/'] = div
		self['^'] = pow
		self['>'] = gt
		self['<'] = lt
		self['='] = eq
		self['!='] = neq
		self['>='] = gteq
		self['<='] = lteq
		self['get'] = get
		self['set'] = set
		self.state_data = Dict()
		self.world_attr = Dict()
		self.world_data = Dict()
		self.value_attr = Dict()
		self.op_classes = Dict({'proposition': ['>', '<', '=', '!=', '>=', '<='],
						          'numerical': ['+', '-', '*', '/', '^'],
						            'logical': ['set', 'get']})

	def assign(self, key, world):
		if key not in self.world_data[world]:
			self.world_data[world].append(key)

	def set_item(self, key, value, world=None, weights=Dict()):
		if world != None: self.assign(key, world)
		attr = Dict({'world': world,
					 'weights': weights,
					 'type': self.identify(value)})
		self.value_attr[key] = attr
		self[key] = value
		self.state_data[key] = 0
	def get_item(self, item, attr=None):
		if attr != None: y = self.value_attr[item][attr]
		else: y = self[item]
		return y

	def set_world(self, world, lower_limit=0.001, upper_limit=0.8, min_size=1, max_size=10):
		attr = Dict({'lower_limit': lower_limit,
					 'upper_limit': upper_limit,
					 'min_size': min_size,
					 'max_size': max_size})
		self.world_attr[world] = attr
		self.world_data[world] = []
	def get_world(self, world, attr=None):
		w = self.translate(self.world_data[world])
		if attr != None: y = self.world_attr[world][attr]
		else: y = w
		return y

	def worlds(self):
		return self.world_data.keys()

	# def insert(self, world, key):
	# 	if self.get_world(world) == None:
	# 		self.set_world(world)
	# 		value = None
	# 		if key in self.keys():
	# 			value = self[key]				
	# 	if key not in self.weights:
	# 		self.weights[key] = Dict()
	# 		self.biases[key] = rr(1,10)/100
	# 	self.worlds[world].append(key)
	
	# # def remove(self, world, key):
	# # 	index = self.worlds[world].index(key)
	# # 	del self.worlds[world][index]
	# # 	del self.biases[key]
	# # 	del self.weights[key]
	# # 	if world != 'unassigned':
	# # 		self.insert('unassigned', key)

	# # def generate(self, world):
	# # 	inputs = []
	# # 	options = self.get_world(world)
	# # 	if len(options) < self.limits[world][0]:
	# # 		if world-1 in self.worlds.keys():
	# # 			selection = self.generate(world-1)
	# # 		else:
	# # 			selection = rr(2)
	# # 	else:
	# # 		for j in range(rr(2, 5)):
	# # 			k = rr(len(options))
	# # 			x = options[k]
	# # 			inputs.append(x)
	# # 		functions = ['>','<','=', '>=', '<=', '+', '-', '*', '^']
	# # 		options = []
	# # 		for f in functions:
	# # 			pattern = tuple([f] + inputs)
	# # 			options.append(pattern)
	# # 		selection = options[rr(len(options))]
	# # 	return selection

	def classify(self, key):
		for i in self.op_classes.keys():
			if key in self.op_classes[i]:
				return i

	def update(self, world):
		lower_limit = self.get_world(world, 'lower_limit')
		upper_limit = self.get_world(world, 'upper_limit')
		lower_bound = self.get_world(world, 'min_size')
		upper_bound = self.get_world(world, 'max_size')
		world_values = self.get_world(world)
		world_output = 0
		
		for i in range(len(world_values)):
			v = world_values[i]
			y = 0
			if self.identify(self.translate(v)) == 'pattern':
				f = v[0]
				x = v[1:]
				b = self.biases[v]
				
				# if self.classify(f) == 'proposition':

		# 			if f(x): y = 1
		# 			else: y = -1
		# 			y *= b
		# 	world_output += y

		# world_output = tanh(world_output)
		# world_reward = logistic(size - lower_bound) + logistic(upper_bound - size)
		
#######################################################################################################		
		total = 0
		count = 0
		score = 0
		outputs = []
		keys = self.keys()
		data = list(self.values())
		for i in range(len(data)):
			x = data[i]
			k = keys[i]
			y = -1 / (1/2 * len(data))
			if self.identify(self.translate(k)) == 'pattern':
				try:
					y += self.compute(x)
				except:
					y = -1
				if y in [True, False]:
					if y == True: x = 1
					if y == False: x = -1
			y *= self.biases[k]
			outputs.append(y)
			total += y
		score = logistic(sum(outputs))

		to_remove = []
		to_reduce = []
		to_assign = []
		for i in range(len(data)):
			k = keys[i]
			b = self.biases[k]
			db = 0.1 * outputs[i] * score * (1-tanh(abs(b)))
			self.biases[k] = b + db
			if self.thresholds[world] != None:
				if self.identify(self.translate(k)) == 'pattern':
					if self.biases[k] < self.thresholds[world]:
						to_remove.append(k)
					elif self.biases[k] > .01:#-self.thresholds[world]:
						to_reduce.append(k)

		if world+1 in self.worlds.keys():
			for i in range(len(to_reduce)):
				key = to_reduce[i]
				pattern = self.compress(key)
				self.remove(world, key)
				self[random_str(5-world)] = pattern, world+1

		if self.limits[world][0] != None:
			if len(data)-len(to_remove) > self.limits[world][0]:
				for i in to_remove:
					self.remove(world, i)

		if self.limits[world][1] == None or len(data) < self.limits[world][1]:
				unassigned = self.worlds['unassigned']
				if len(unassigned) > 0:
					key = unassigned[rr(len(unassigned))]
					self.remove('unassigned', key)
				else:key = random_str(4)
				self[key] = self.generate(world), world
		return score

	def measure(self, pattern):
		X = []
		pattern = self.translate(pattern)
		if self.identify(pattern) != 'pattern':
			return pattern
		for i in range(1, len(pattern)):
			x = self.translate(pattern[i])
			if self.identify(x) == 'pattern': 
				x = self.measure(x)
			X.append(x)
		return X

	def execute(self, pattern, data=None):
		root = False
		if data == None:root = True
		if root: data = Dict()
		pattern = self.compress(pattern)
		derivatives = []
		output = self.measure(pattern)
		D = 0
		if isinstance(output, list):
			y = output[0]
			X = output[1]
			D = 0
			output = []
			for x in X:
				dx = x 
				if self.identify(data) in ['int', 'float']:
					dx *= data
				dx /= y
				output.append(dx)
				D += dx
		return output

memory = EquationMemory()

memory.set_item('y', ('+', 'b', ('*', 'm', 'x')))
memory.set_item('m', 4)
memory.set_item('x', 2)
memory.set_item('b', 3)
f = memory.execute('y', 5)

worlds = 5
for i in range(worlds):
	world = i
	threshold = 1/pow(worlds-world, 2)
	min_size = 3
	max_size = 3 * (worlds-world)
	memory.set_world(world, threshold, min_size, max_size)

ops = ['>','<','=']
pro = ['>','<','=']

inputs = []
for i in range(5):
	key = random_str(4)
	value = rr(2)
	memory[key] = value, 0

log = open('log.txt', 'w')
for i in range(1000):
	s = str(i) + '	'
	c = 0
	worlds = memory.worlds()
	for j in range(len(worlds)):
		score = memory.update(j)
		limit = memory.get_world(j, 'upper_limit')
		

		world = memory.get_world(j)
		s += str(score) + '	'
		c += 1
	print(s)
	log.write(s + '\n')
log.close()
