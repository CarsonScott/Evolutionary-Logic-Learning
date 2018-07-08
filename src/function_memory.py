from pattern_memory import *
from probability_distribution import *
from template import *

class Agent(PatternMemory): 
	def construct(self, operator, *variables):
		return template(operator, variables)

	def generate(self, expression):
		return generate(expression)(self)
		# print(self.parser.parse(expression))


space = JointProbability([str(i) for i in range(10)], 10)
keys = space.keys()

options = Matrix(keys)
pattern = []

for i in range(10):
	x = options[rr(len(options))]
	del options[options.index(x)]
	pattern.append(x)

print(pattern)
p = 0
for i in range(100000):
	x = pattern[p]
	p += 1
	if p == len(pattern):
		p = 0
		print()
	space.append(x)
	print(x, reverse(sort(space.compute(x)))[0:int(len(space.keys())/3)])

for x in keys:
	output = space.compute(x)
	output = sort(output)
	string = str(x) + '	' + str(output)
	# for k in keys:
	# 	value = output[k]
	# 	string += str(value) + '	'
	print(string)

if __name__ == "__main__":
	agent = Agent()
	agent['a'] = 1
	agent['b'] = 1
	agent['c'] = agent.construct('+', 'a', 'b')

	y = agent.construct('+', 'a', 'b')
	print(agent.generate('(a ^ b);'))
	# print(is_template(y))
	# class FunctionMemory(PatternMemory):
	# 	def construct(self, data):
	# 		data = self.translate(data)
	# 		model = Model(data)
	# 		return model

	# 	def identify(self, data):
	# 		if isinstance(data, Model):
	# 			return 'model'
	# 		return super().identify(data)

	# 	def convert(self, key):
	# 		self[key] = self.construct(key)

	# 	def __call__(self, data):
	# 		if self.identify(self.translate(data)) == 'pattern':
	# 			data = self.translate(data)
	# 			if self.identify(self.translate(data[0])) == 'model':
	# 				f = self[data[0]].get_function()
	# 				f = self.translate(data[0]).get_function()
	# 				x = self.translate(data[0]).get_inputs()
	# 				data = tuple([f] + x)
	# tuple([f] + x)		return super().__call__(data)
		

	# mem = FunctionMemory()
	# mem['a'] = ('^', 'b', 'c')
	# mem['b'] = 5
	# mem['c'] = 3
	# mem['d'] = 3
	# mem.convert('a')

	# y = mem(('a', 'b', 'd'))
	# print(y)
