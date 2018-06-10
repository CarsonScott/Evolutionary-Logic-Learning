from template import addition, create, generate, express, ExpressionTree
from goodata import Dict
from random import randrange as rr
from lib.relations import *
from math import tanh

class Proposition:
	def __init__(self, data):
		self.data = data
		self.create()
	def create(self):
		data = self.data
		self.expression = None
		self.function = None
		if isinstance(data, str):
			self.expression = data
			self.function = generate(data)
		elif isinstance(data, Proposition):
			self.expression = express(data)
			self.function = data
		self.template = ExpressionTree(self.expression)
	def __call__(self, input):
		self.create()
		return self.function(input)

Proposition('(a conjunction b);')

class Pattern(list):
	def __init__(self, propositions=[]):
		for p in propositions:
			self.append(p)
	def __call__(self, X):
		Y = []
		for f in self:
			Y.append(f(X))
		return Y
	def size(self):
		return len(self)

class System:
	def __init__(self, patterns=[]):
		self.patterns = patterns
		self.database = Dict()
		for i in range(len(self.patterns)):
			self.add(self.patterns[i])
	def size(self):
		return len(self.patterns)
	def add(self, pattern):
		index = self.size()
		self.patterns.append(pattern)
		self.database[index] = Dict()
	def combine(self, I):
		P = []
		for i in I:
			P = union(P, p)
		return Pattern(p)
	def compare(self, i, j):
		P = intersection(self.patterns[i], self.patterns[j])
		return Pattern(P)

def random_subset(X, s):
	Y = []
	V = []
	for x in X:
		V.append(x)

	for i in range(s):
		j = rr(len(V))
		Y.append(V[j])
		del V[i]
	return Y
