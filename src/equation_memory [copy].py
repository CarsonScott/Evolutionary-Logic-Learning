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
		self.thresholds = Dict()
		self.weights = Dict()
		self.limits = Dict()
		self.biases = Dict()
		self.worlds = Dict()
		self.roots = Dict()
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
		self['store'] = self.__setitem__

	def __setitem__(self, key, *data):
		x = list(data)
		world = None
		if isinstance(x[0], tuple):
			value, world = x[0]
			# self.insert(world, key)
		else:value = x[0]
		super().__setitem__(key, value)

	def set_weight(self, source, target, weight=1):
		self.weights[source][target] = weight
	def get_weight(self, source, target):
		if target in self.weights[source].keys():
			return self.weights[source][target]
		return None

	def get_world(self, world):
		if world in self.worlds.keys():
			return self.worlds[world]

	def set_world(self, world, threshold=0.001, limit=(3, 20)):
		self.worlds[world] = []
		self.thresholds[world] = threshold
		self.limits[world] = limit

	def insert(self, world, key):
		if world not in self.worlds.keys():
			self.set_world(world)
		if key not in self.get_world(world):
			self.worlds[world].appen
		self.worlds[world].append(key)
	
	def remove(self, world, key):
		index = self.worlds[world].index(key)
		del self.worlds[world][index]
		del self.biases[key]

	def generate(self, world):
		inputs = []
		options = self.get_world(world)
		if len(options) < self.limits[world][0]:
			if world-1 in self.worlds.keys():
				selection = self.generate(world-1)
			else:selection = rr(2)
		else:
			for j in range(rr(2, 5)):
				k = rr(len(options))
				x = options[k]
				inputs.append(x)
			functions = ['>','<','=', '>=', '<=', '+', '-', '*', '^']
			options = []
			for f in functions:
				pattern = tuple([f] + inputs)
				options.append(pattern)
			selection = options[rr(len(options))]
		return selection

	def update(self, world):
		keys = self.get_world(world)
		data = self.translate(keys)
		total = 0
		count = 0
		score = 0
		outputs = []
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
			
			if k in self.biases.keys():
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
				self[random_str(3)] = pattern, world+1

		if self.limits[world][0] != None:
			if len(data)-len(to_remove) > self.limits[world][0]:
				for i in to_remove:
					self.remove(world, i)

		if self.limits[world][1] == None or len(data) < self.limits[world][1]:
				key = random_str(4)
				self[key] = self.generate(world), world
				print(self.biases[key])
		return score

memory = EquationMemory()

worlds = 5
for i in range(worlds):
	threshold = 1/pow(worlds-i, 2)
	min_capacity = 3
	max_capacity = 3 * (worlds-i)
	memory.set_world(i, threshold,(min_capacity, max_capacity))

inputs = []
for i in range(5):
	key = random_str(3)
	value = rr(2)
	memory[key] = value, 0

log = open('log.txt', 'w')
for i in range(1000):
	s = str(i) + '	'
	c = 0
	for j in range(len(memory.worlds.keys())):
		print(memory.worlds[4])
		score = memory.update(j) / memory.limits[j][1]
		world = memory.get_world(j)
		s += str(score) + '	'
		c += 1
	#print(s)
	log.write(s + '\n')
log.close()


world = memory.worlds[0]
for x in world:
	print(x, memory.biases[x], memory.translate(x))