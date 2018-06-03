from lib.util import *
from lib.relations import *

def normalize(value, lower=0, upper=1):
	if value != None:
		if value < lower:
			return lower
		if value > upper:
			return upper
	return value

class Learner:
	def __init__(self, pattern=[], example=[], threshold=0.02, increment=0.02):
		self.pattern = None
		self.example = None
		self.weights = None
		self.positive = None
		self.negative = None
		self.variables = None
		self.strengths = None
		self.increment = increment
		self.threshold = threshold
		self.init(pattern, example)

	def append(self, index):
		if index not in self.weights.keys():
	
			if index in self.pattern:
				self.weights[index] = 1
			else:self.weights[index] = None
			
			if index in self.positive:
				self.strengths[index] = 0.5
			else:self.strengths[index] = 0
		
		elif self.weights[index] == None:
			if index in self.pattern:
				self.weights[index] = rr(10)/10

	def remove(self, index):
		if index in self.weights.keys():
			self.weights[index] = None

	def init(self, pattern=None, example=None):
		if pattern == None:
			pattern = self.pattern
		if example == None:
			example = self.example

		if self.pattern == None:
			self.pattern = list()
		if self.example == None:
			self.example = list()

		if not equivalent(pattern, self.pattern):
			self.pattern = pattern
		if not equivalent(example, self.example):
			self.example = example
		
		reference = compliment(pattern, example)
		inputs = compliment(example, pattern)
		
		self.variables = union(pattern, example)
		self.positive = intersection(pattern, example)
		self.negative = union(reference, inputs)
		
		if self.weights == None:
			self.weights = Dict()
			self.strengths = Dict()
		
		for i in range(len(self.variables)):
			self.append(self.variables[i])

	def score(self, index):
		weight = self.weights[index]
		
		if weight == None:weight = 1
		score = weight * 1/len(self.variables)
		
		if index in self.positive:return score
		elif index in self.negative:return -score

	def utility(self):
		utility = 0
		for i in range(len(self.variables)):
			index = self.variables[i]
			utility += self.score(index)
		return utility

	def strength_deltas(self):
		deltas = Dict()
		
		for i in range(len(self.variables)):
			index = self.variables[i]
			strength = self.strengths[index]
			score = self.score(index)

			delta = score
			if index in self.example:
				delta = abs(score)
			deltas[index] = delta

		return deltas

	def weight_deltas(self):
		deltas = Dict()
		utility = self.utility()
		for i in range(len(self.variables)):
			index = self.variables[i]
			score = self.score(index)
			
			delta = 0
			if index in self.pattern:
				delta = score * utility
			deltas[index] = delta
		return deltas

	def revise(self):
		for i in self.strengths.keys():
			strength = self.strengths[i]
			
			if strength >= self.threshold:
				if i not in self.pattern:
					self.pattern.append(i)
					self.append(i)
			
			elif strength < -self.threshold:
				if i in self.pattern:
					del self.pattern[self.pattern.index(i)]
					self.remove(i)

	def update(self):
		strength_deltas = self.strength_deltas()
		weight_deltas = self.weight_deltas()
		
		for i in range(len(self.variables)):
			index = self.variables[i]
			dw = weight_deltas[index]
			ds = strength_deltas[index]

			self.strengths[index] += ds * self.increment
			if self.weights[index] != None:	
				self.weights[index] += dw * self.increment

			self.weights[index] = normalize(self.weights[index], 0, 2)
			self.strengths[index] = normalize(self.strengths[index], -2, 2)
		
	def train(self, observation=None, increment=None):
		prev_inc = self.increment
		if increment == None:
			increment = self.increment
		
		self.revise()
		self.update()
		
		self.increment = prev_inc
		self.init(example=observation)

	def test(self, observation=None):
		prev_obs = self.example
		self.init(example=observation)

		utility = self.utility()
		self.init(example=prev_obs)
		return utility