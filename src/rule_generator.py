from pattern import *
from function import *
from lib.data import *
from templates.ordering import *
from lib.relations import *

class Sequence(list):
	
	def translate(self):
		return merge('.', self)

	def relate(self, function=intersection):
		relations = Sequence()
		for i in range(1, len(self)):
			previous = self[i-1]
			current = self[i]
			if not isinstance(previous, list):
				previous = [previous]
			if not isinstance(current, list):
				current = [current]
			relation = function(previous, current)
			relations.append(relation)
		return relations

class RuleGenerator(Dict):
	def __init__(self, threshold, learning_rate=0.001):
		super().__init__()
		self.lrate = learning_rate
		self.threshold = threshold

	def translate(self, keyword):
		y = str(keyword).split('.')
		return y

	def compute(self, record):
		active = record['active']
		predicted = record['predicted']
		performance = record['performance']

		if len(active) > 0:
			pattern = Matrix(active)
			inference = predicted[len(predicted)-1]
			keyword = merge('.', pattern)
			if performance > self.threshold:
				if keyword not in self.keys():
					self[keyword] = Dictionary()
				if inference not in self[keyword].keys():
					self[keyword][inference] = 0
				self[keyword][inference] += logistic(performance)

	def generate(self):
		rules = Dictionary()
		for i in self.keys():
			pattern = self.translate(i)
			total = sum(list(self[i].values()))
			threshold = self.threshold
			keys = self[i].keys()
			for k in keys:
				if threshold < self[i][k] / total:
					if k not in rules:rules[k] = Dictionary() 
					for j in self.translate(i):
						rules[k][j] = None
		return rules
