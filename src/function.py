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
		
class Transformation(Matrix):
	def __init__(self, size=0):
		super().__init__([[], [], []])
		for i in range(size):
			self.append()
	def append(self, *X):
		x = 0
		b = 0
		m = 0
		if len(X) == 3:x,m,b = X
		if len(X) == 2:x,m = X
		if len(X) == 1:x = X
		self[1].append(x)
		self[0].append(m)
		self[2].append(b)
	def compute(self):
		X = associate(*list(self))
		Y = Matrix()
		for i in X:
			x, m, b = i
			y = m * x + b
			Y.append(y)
		return Y

class Iterator(Function):
	def __init__(self, iterator=None, function=None):
		super().__init__(function)
		if iterable(iterator):
			self.iterator = Matrix(iterator)
		elif identify(iterator) == 'int':
			self.iterator = compose([iterator])
		else:self.iterator = None
		self.index = -1
		self.total = 0

	def iterate(self):
		self.index += 1
		if self.iterator == None:
			return self.index
		elif self.index < len(self.iterator):
			return self.iterator[self.index]
		else:self.index = 0

	def update(self):
		if self.index != None:
			if self.iterator == None:
				return self.index
			elif self.index < len(self.iterator):
				return self.iterator[self.index]

	def __call__(self):
		i = self.iterate()
		x = self.update()
		if x == None:
			self.index = 0
		self.total += 1
		output = self.index
		if self.function != None:
			output = super().__call__(output)
		return output