from pattern_memory import *

class Model(Dict):
	def __init__(self, variables):
		for k in variables:
			self[k] = None

	def get_inputs(self, key):
		if key not in self.open:
			self.open.append(key)

	def get_open(self):
		re
class ModelMemory(PatternMemory):
	def __init__(self):
		self.constraints = Dict()

model = Model(['a', 'b', 'c'], ['a', 'c'])