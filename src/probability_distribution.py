from rule_generator import *
from function_template import *
import matplotlib.pyplot as plt

class Generator(Dictionary):
	pass

class Iterator(Generator):
	def __call__(self, X=None):
		if 'data' not in self:
			self['data'] = False
		self['data'] = not self['data']
		return self['data']

class Random(Generator):
	def __call__(self, X=None):
		self['data'] = rr(10)
		return self['data']

class Counter(Iterator):
	def __call__(self, X):
		if 'data' not in self:
			self['measure'] = False
			self['count'] = 0
		self['data'] = X
		self['count'] = self['count'] + self['data']
		return self['count']

class Detector(Generator):
	def __call__(self, X):
		if 'measure' not in self:
			self['measure'] = False
			self['memory'] = False
		self['measure'] = X
		self['data'] = self['measure'] is not self['memory']
		self['memory'] = self['measure']
		return self['data']

template = Function(statement='y=count(g)', inputs=['x'])
template['detect'] = Detector()
template['count'] = Counter()
template['iterate'] = Iterator()
template['g'] = 'detect(h)'
template['h'] = 'iterate(x)'
template['x'] = None

for i in range(100):
	y = template(rr(100))
	print(y)

class Signal(Matrix):
	def __init__(self, size, memory):
		self.memory = Matrix([0 for i in range(memory)])
		for i in range(size):
			self.append(0)
	def __call__(self, value):
		total = 0
		for i in range(len(self)):
			value = self[i] + tanh(1-abs(math.ceil(self[i]) - self[i]))/2
			if i > round(value): 
				self[i] = 0
			self[i] = value
		self.memory.append(Matrix(self))
		del self.memory[0]
		return self

sm = Signal(10, 5)

inputs = ['a', 'b', 'c', 'd', 'e', 'f', 'b', 'h', 'i', 'j']
pattern = Pattern(4, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
learner = RuleGenerator(0.9)

for j in range(1000):
	for i in range(len(inputs)):
		record = pattern(inputs[i])
		learner.compute(record)

rules = learner.generate()
order = Ordering(inputs)

for y in rules.keys():
	for x in rules[y].keys():
		order.order(x,y)

for i in range(1, len(inputs)):
	x1 = inputs[i-1]
	x2 = inputs[i]
	print(x1, x2, order(x1, x2))

class Agent(Function):
	def __init__(self):
		super().__init__()
		
	def set(self, X):
		k = None
		v = None
		for x in X:
			if k == None:
				k = x
			elif v == None:
				v = x
				self[k] = v
				v = None
				k = x

	def get(self, X):
		Y = []
		k = None
		y = None
		for x in X:
			if k == None:
				k = x
				y = self[k]
				Y.append(y)
				k = None
				y = None
		if len(Y) == 1:Y = Y[0]
		return Y

	def signal(self, key, size, memory):
		signal = Signal(size, memory)
		self[key] = signal

	def generator(self, key, threshold, learningrate):
		generator = RuleGenerator(threshold, learningrate)
		self[key] = generator

	def template(self, key, parameters=None):
		template = Function()
		self[key] = template

agent = Agent()
agent.signal('sig1', 10, 5)
agent.generator('gen1', 0.9, .001)
agent.template('tem1')
