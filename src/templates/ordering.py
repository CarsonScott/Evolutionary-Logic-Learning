from dictionary import *

class Ordering(Dictionary):
	def __init__(self, variables):
		super().__init__()
		self + variables
		for v in variables:
			self[v] = Dictionary()
	def order(self, *variables):
		for i in range(len(variables)-1):
			for j in range(i+1, len(variables)):
				X = variables[i]
				Y = variables[j]
				if X not in self:
					self[X] = Dictionary()
				if Y not in self:
					self[Y] = Dictionary()

				if X != Y:
					if Y not in self[X]:
						self[X][Y] = None
					if X in self[Y]:
						del self[Y][X]
	def compare(self, *variables):
		for i in range(len(variables)-1):
			for j in range(i+1, len(variables)):
				X = variables[i]
				Y = variables[j]
				if identify(X) == 'list':
					for k in range(len(X)):
						x = X[k]
						if identify(Y) == 'list':
							y = Y[k]
							if self.compare(x, y):
								return False
						else:
							if self.compare(x, Y):
								return False
				else:
					if Y not in self[X] :
						return False
		return True

	def __call__(self, *variables):
		return self.compare(*variables)