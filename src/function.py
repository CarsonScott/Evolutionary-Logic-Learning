from matrix import *

class Function(Matrix):
	def __init__(self, matrix=[]):
		super().__init__(matrix)
		self.indices = Dict()
		self.private = Dict()
		for i in range(len(matrix)):
			x,y = matrix[i]
			self.set(x, y)
	def get(self, input):
		if input in self.indices.keys():
			return self.indices[input]
		return input
	def set(self, input, output):
		index = len(self)
		self.append(create(input, output))
		if input not in self.indices.keys():
			self.indices[input] = create()	
		self.indices[input].append(index)
	def index(self, input):
		index = self.get(input)
		return index
	def output(self, index):
		output = self[index, 1]
		return output
	def __call__(self, input):
		indices = self.index(input)
		outputs = Matrix()
		if iterable(indices):
			for i in indices:
				output = self.output(i)
				outputs.append(output)
		if len(outputs) == 1:
			outputs = outputs[0]
		return outputs
