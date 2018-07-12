from pattern import *
from function import *

class RuleLearner(Function):
	def __init__(self, threshold, pattern=None, learning_rate=0.01):
		self.lrate = learning_rate
		self.threshold = threshold
		self.pattern = pattern
		super().__init__()

	def translate(self, keyword):
		y = str(keyword).split('.')
		return y

	def compute(self, input):
		record = self.pattern(input)
		active = record['active']
		predicted = record['predicted']
		performance = record['performance']

		if len(active) > 0:
			pattern = Matrix(active)
			inference = predicted[len(predicted)-1]
			keyword = merge('.', pattern)
			if performance > self.threshold:
				self.set(keyword, inference)
			return keyword