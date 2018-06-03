class Memory:
	def __init__(self, variables):
		self.variables = [False for i in range(variables)]
		self.previous = self.variables

	def update(self):
		active = []
		for i in range(len(self.variables)):
			variable = self.variables[i]
			previous = self.previous[i]

			if variable == True:
				active.append(i)
				self.variables[i] = False

		self.previous = self.variables
		return active