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

