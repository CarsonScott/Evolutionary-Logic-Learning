from pattern_memory import *
from lib.util import *

class Model(PatternMemory):
	def __init__(self, pattern):
		super().__init__()
		X = []
		function = pattern[0]
		inputs = list(pattern[1:])
		for i in range(len(inputs)):
			x = inputs[i]
			if x not in self.keys():
				self[x] = None
			X.append(x)
		self['/output'] = None
		self['/pattern'] = [function] + inputs
	def get_pattern(self):
		return self.translate('/pattern')
	def get_size(self):
		return len(self.get_pattern())
	def get_inputs(self):
		return self.get_pattern()[1:]
	def get_function(self):
		return self.get_pattern()[0]
	def get_output(self):
		return super().compute(tuple(self.get_pattern()))
	def set_output(self, value):
		self['/output'] = value

	def update(self, values):
		inputs = self.get_inputs()
		print(inputs, values)
		c = 0
		for i in inputs:
			self[i] = values[c]
			c += 1

	def signature(self):
		sig = Dict()
		sig['type'] = self.translate(self.get_function())
		sig['args'] = tuple(self.get_inputs())
		return sig

	def __call__(self, values):
		self.update(values)
		output = self.get_output()
		self.set_output(output)
		return output