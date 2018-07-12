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
	def set(self, input, output):
		if input not in self.indices.keys():
			index = len(self)
			self.indices[input] = [index]	
			self.append(Matrix([input, output]))
		else:
			indices = self.indices[input]
			recorded = False
			for i in indices:
				if self.output(i) == output:
					recorded = True
			if not recorded:
				self.indices[input].append(len(self))
				self.append(Matrix([input, output]))

	def index(self, input):
		index = self.get(input)
		return index
	def output(self, index):
		output = self[index, 1]
		return output
	def __call__(self, input):

		i = self.index(input)
		if i == None:return None
		Y = []
		if len(i) > 1:
			for j in i:Y.append(self.output(j))
		elif len(i) == 1:Y = self.output(i[0])
		return Y
		