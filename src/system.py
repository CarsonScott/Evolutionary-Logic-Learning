from lib.util import *
from lib.relations import *
from learner import *
import math

def random_subset(set, size):
	X = list(set)
	Y = list()
	for i in range(size):
		if len(X) > 0:
			index = rr(len(X))
			value = X[index]
			del X[index]
			Y.append(value)
		else:break
	return Y

class MemorySystem:
	def __init__(self, variables, learners, threshold, increment):
		self.variables = variables
		self.threshold = threshold
		self.increment = increment
		self.urgencies = list()
		self.utilities = list()
		self.learners = list()
		for i in range(learners):
			self.learners.append(Learner(threshold=threshold, increment=increment))
			self.urgencies.append(.1)
			self.utilities.append(0)
		self.init()

	def init(self):
		for	i in range(len(self.learners)):
			size = rr(int(len(self.variables) * .115), int(len(self.variables)))
			print(random_subset(self.variables, size))
			self.learners[i].init(pattern=random_subset(self.variables, size))

	def rank(self, example):
		utilities = []
		for i in range(len(self.learners)):
			utilities.append(self.learners[i].test(example))
		return utilities

	def revise(self, index, utility):
		self.urgencies[index] += self.increment * utility * self.urgencies[index]

	def states(self, utilities):
		states = []
		for i in range(len(utilities)):
			state = utilities[i]
			delta = -self.urgencies[i]
			for j in range(len(utilities)):
				if i != j:
					delta -= utilities[j]
			state += delta * self.increment
			states.append(state)
		return states

	def train(self, example):
		ranks = self.rank(example)
		states = self.states(ranks)
		order = reverse(sort(states))
		index = order[0]
		best = states[index]

		if best  < self.threshold:
			empty = []
			sizes = []
			for i in range(len(self.learners)):
				sizes.append(len(self.learners[i].pattern))
			order = sort(sizes)
			sample = order[0:int(len(order)/3)]
			index = order[rr(len(sample))]

		performance = 0
		for i in range(len(self.learners)):
			rank = ranks[i]
			place = order.index(i)
			total = len(order)
			
			if i == index: 
				observation = example
			elif self.urgencies[i] < 0:
				observation = []
			else:observation = self.learners[i].example
			self.learners[i].train(observation)

			utility = self.learners[i].utility()
			self.utilities[i] = utility
			self.revise(i, utility)
			performance += utility

		return performance


variables = list('abcdefghijklmnopqrstuvwxyz')
learners = 3
threshold = 0.002
increment = 0.0001

system = MemorySystem(variables, learners, threshold, increment)
X = [
	list('world'),
	list('howdy'),
	list('carson')
]

log = open('log.txt', 'w')

c = -1
count = 0
for i in range(100000):
	c += 1
	if c == len(X):
		c = 0
		count += 1
		if count % 100 == 0:
			print(count)

	x = X[c]
	y = system.train(x)

	for j in range(len(system.learners)):
		print(system.learners[j].pattern)

	log.write(str(j) + '	' + str(y) + '\n')
	# print(system.urgencies)
	# p = ms.learners[y].pattern
	# equal = equivalent(x, p)
	
	# if equal:
	# 	print('success')
	# else:
	# 	print('...')
	# print('\nobserved example:', x, '\nselected learner:', p, '\n		', equivalent(x, p))
log.close()
# class System:
# 	def __init__(self, var_size, mem_size):
# 		self.network = Network(var_size)
# 		self.memory = Memory(var_size)
# 		self.stream = Stream(mem_size)
# 		self.inc = 0.001

# 	def __setitem__(self, index, value):
# 		self.memory.variables[index] = value

# 	def __getitem__(self, index, value):
# 		self.memory.variables[index] = value

# 	def activate(self, variables):
# 		for i in variables:
# 			self[i] = True

# 	def update(self):
# 		active = self.memory.update()
# 		stores = self.stream.update(active)
# 		for i in range(len(stores)):
# 			store = stores[i]
# 			inc = self.inc * (1 - i/len(self.stream.stores))
# 			self.network.train(store, inc)
# 		return stores
		
# var_count = 5
# mem_count = 3
# system = System(var_count, mem_count)

# for i in range(1000):
# 	if i % 10 == 0:
# 		a = rr(var_count)
# 		b = rr(var_count)
# 		system.activate([a, b])
# 	system.update()
# 	print_network(system.network)
