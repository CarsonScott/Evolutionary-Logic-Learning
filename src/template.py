from lib.functions import *
from lib.relations import *
from lib.constraints import *
from lib.util import *

class GroupedSet(list):
	def __init__(self, groups, default=None):
		self.groups = groups
		self.default =default
		size = len(union(groups, groups))
		for size in range(size):
			self.append([])
	def __call__(self, inputs):
		visited = []
		for i in range(len(inputs)):
			if i < len(self.groups):
				g = self.groups[i]
	
			elif self.default != None:
				g = self.default

			if g != None:		
				if g not in visited:
					self[g] = []
					visited.append(g)
				x = inputs[i]
				self[g].append(x)
		return self

def to_string(X):
	string = ''
	for x in X:
		string += str(x)
	return string

def product(X):
	y = X[0]
	for i in range(1, len(X)):
		y *= X[i]
	return y

def is_template(object):
	return isinstance(object, Dict) and containment(['type', 'data'], object.keys())

def template(type=None, data=None):
	return Dict({'type':type, 'data':data})

def association(group=None):
	output = template('conjunction')
	output['group'] = group
	return output

def addition(group=None):
	output = template('addition')
	output['group'] = group
	return output
def subtraction(group=None):
	output = template('subtraction')
	output['group'] = group
	return output
def multiplication(group=None):
	output = template('multiplication')
	output['group'] = group
	return output
def division(group=None):
	output = template('division')
	output['group'] = group
	return output

def implication(group):
	premise, conclusion = group
	if conclusion == None and isinstance(premise, tuple):
		conclusion = premise[0]
		premise = premise[1]
	output = template('implication')
	output['premise'] = premise
	output['conclusion'] = conclusion
	return output

def create(type, data):
	return template(type, data)

def convert(template):
	type = template['type']
	data = template['data']

	for i in range(len(data)):
		if is_template(data[i]):
			data[i] = convert(data[i])
		else:
			try:
				if int(data[i]) == float(data[i]):
					data[i] = int(data[i])
				else:
					data[i] = float(data[i])
			except:
				data[i] = data[i]

	if type in CONNECTIVE_NAMES:
		index = CONNECTIVE_NAMES.index(type)
		return CONNECTIVE_FUNCTIONS[index](data)

class Proposition:
	def __call__(self, memory):
		return

class Truth(Proposition):
	def __init__(self, variable):
		self.variable = variable
	def __call__(self, memory):
		return self.variable in memory.keys() and memory[self.variable] == 1

class Implication(Proposition):
	def __init__(self, pair):
		self.premise = pair[0]
		self.conclusion = pair[1]
	def __call__(self, memory):
		premise = self.premise
		if not isinstance(self.premise, Proposition):
			premise = Truth(premise)
		output = None
		if premise(memory):
			conclusion = self.conclusion
			if not isinstance(self.conclusion, Proposition):
				conclusion = Truth(conclusion)
			output = conclusion(memory)
		return output

class Conjunction(Proposition):
	def __init__(self, group):
		self.group = group
	def __call__(self, memory):
		group = self.group
		for i in range(len(group)):
			data = group[i]
			if not isinstance(data, Proposition):
				data = Truth(data)
			group[i] = data(memory)
		output = product(group)
		return bool(output)

class Disjunction(Proposition):
	def __init__(self, group):
		self.group = group
	def __call__(self, memory):
		group = self.group
		for i in range(len(group)):
			data = group[i]
			if not isinstance(data, Proposition):
				data = Truth(data)
			group[i] = data(memory)
		output = sum(group) > 0
		return bool(output)

GRAMMAR_SYMBOLS = ['(', ')', ';', ' ']
CONNECTIVE_SYMBOLS = ['^', '|', '<']
CONNECTIVE_NAMES = ['conjunction', 'disjunction', 'implication']
CONNECTIVE_FUNCTIONS = [Conjunction, Disjunction, Implication]

def initialize(connectives):
	connective_names = []
	connective_symbols = []
	connective_functions = []
	keys = list(connectives.keys())
	for i in keys:
		name = i
		symbol = connectives[i]['symbol']
		function = connectives[i]['function']
		connective_names.append(name)
		connective_symbols.append(symbol)
		connective_functions.append(function)
	return connective_names, connective_symbols, connective_functions

def express(proposition, marker=';'):
	string = '('
	if isinstance(proposition, Truth):
		string += str(proposition.variable)

	elif isinstance(proposition, Implication):
		premise = proposition.premise
		conclusion = proposition.conclusion
		if isinstance(premise, Proposition):
			premise = express(premise, '')
		if isinstance(conclusion, Proposition):
			conclusion = express(conclusion, '')

		index = CONNECTIVES.index(Implication)
		symbol = CONNECTIVE_SYMBOLS[index]
		string += str(premise) + ' ' + symbol + ' ' + str(conclusion)

	elif isinstance(proposition, Conjunction):
		group = proposition.group
		if isinstance(group[0], Proposition):
			group[0] = express(group[0], '')
		string += str(group[0])

		index = CONNECTIVES.index(Conjunction)
		symbol = CONNECTIVE_SYMBOLS[index]
		for i in range(1, len(group)):
			string += ' ' + symbol + ' '
			data = group[i]
			if isinstance(data, Proposition):
				data = express(data, '')
			string += str(data)

	elif isinstance(proposition, Disjunction):
		group = proposition.group
		if isinstance(group[0], Proposition):
			group[0] = express(group[0], '')
		string += str(group[0])
		index = CONNECTIVES.index(Disjunction)
		symbol = CONNECTIVE_SYMBOLS[index]
		for i in range(1, len(group)):
			string += ' ' + symbol + ' '
			data = group[i]
			if isinstance(data, Proposition):
				data = express(data, '')
			string += str(data)
	return string + ')' + marker

class EmbeddedList(list):
	def __init__(self, size, value=None):
		for i in range(size):
			self.append(value)
	def expand(self, index):
		self[index] = EmbeddedList(1, self[index])

class ExpressionTree(EmbeddedList):
	def __init__(self, expression=None):
		super().__init__(0)
		self.state = 0
		if expression != None:
			self.parse(expression)

	def expand(self, index):
		self[index] = ExpressionTree()

	def update(self, character):
		if len(self) == 0:
			self.append(None)

		if character == '(':
			if self.state == 0:
				if self[len(self)-1] != None:
					self.append(None)
				self[len(self)-1] = ExpressionTree()
				self.state = 1
			else:
				y = self[len(self)-1].update(character)
				if y != None:self.state = 0

		elif character == ')':
			if self.state == 0:return self
			else:
				y = self[len(self)-1].update(character)
				if y != None:self.state = 0

		elif character == ';':
			return self

		elif character != ' ':
			if self.state == 0:
				if len(self) == 0 or self[len(self)-1] != None:
					self.append(character)
				self[len(self)-1] = character
			else:
				y = self[len(self)-1].update(character)
				if y != None:self.state = 0

	def parse(self, expression):
		previous = None
		elements = []
		for i in range(len(expression)):
			character = expression[i]
			if character not in CONNECTIVE_SYMBOLS and character not in GRAMMAR_SYMBOLS:
				if previous == None:
					previous = str()
				previous += character

			elif character != ' ':
				if previous != None:
					elements.append(previous)
				elements.append(character)
				previous = None
		expression = elements
		
		for i in range(len(expression)):
			character = expression[i]
			self.update(character)
		return self

def encode(tree):
	for i in range(len(tree)):
		if isinstance(tree[i], ExpressionTree):
			tree[i] = encode(tree[i])
	if len(tree) == 1:
		return tree[0]
	elif len(tree) == 3:
		a,r,b = tree
		if r in CONNECTIVE_SYMBOLS:
			index = CONNECTIVE_SYMBOLS.index(r)
			r = CONNECTIVE_NAMES[index]
		x = [a, b]
		return template(r, x)

def generate(expression):
	tree = ExpressionTree()
	tree.parse(expression)
	template = encode(tree)
	function = convert(template)
	return function

def variables(expression):
	tree = ExpressionTree()
	tree.parse(expression)
	print(tree)

class RelationalMatrix(Dict):
	def __init__(self, keys):
		self.examples = 0
		for i in range(len(keys)):
			ki = keys[i]
			self[ki] = Dict()
			for j in range(i, len(keys)):
				kj = keys[j]
				self[ki][kj] = 0
	def train(self, keys):
		for i in range(len(keys)):
			ki = keys[i]
			for j in range(i, len(keys)):
				kj = keys[j]
				self[ki][kj] += 1
		self.examples += 1
	def compute(self):
		size = self.examples
		distribution = Dict(self)
		keys = self.keys()
		for i in range(len(keys)):
			for j in range(i, len(keys)):
				ki = keys[i]
				kj = keys[j]
				distribution[ki][kj] /= size
		return distribution
	def reset(self):
		self.examples = 0
		for i in range(len(keys)):
			for j in range(len(keys)):
				ki = keys[i]
				kj = keys[j]
				self[ki][kj] = 0

class Group(Dict):
	def __init__(self, keys):
		self.prob_space = ProbabilitySpace(keys)
		self.rel_matrix = RelationalMatrix(keys)
		self.distribution = None
		self.associations = None 

	def train(self, keys):
		self.prob_space.train(keys)
		self.rel_matrix.train(keys)
	def compute(self):
		self.distribution = self.prob_space.compute()
		self.associations = self.rel_matrix.compute()

	def get(self, initial, final):
		y = Dict()
		y['x'] = self.distribution[initial]
		y['y'] = self.distribution[final]
		y['r'] = self.associations[initial][final]
		return y
		

# keys = ['a', 'b', 'c', 'd'] 
# space = ProbabilitySpace(keys)
# joint = RelationalMatrix(keys)

# group = Group(keys)

# X = [['a', 'b', 'c'],
# 	 ['a', 'c'],
# 	 ['b', 'd']]

# c = 0
# for i in range(50):
# 	x = X[c]
# 	c += 1
# 	if c >= len(X): 
# 		c = 0
# 	group.train(x)

# group.compute()
# print(group.get('a', 'b'))
if __name__ == "__main__":

	memory = {'a':0, 'b':1, 'c':1,'d':1}
	expression = '((a | b) < (c ^ d));'
	function = generate(expression)
	output = function(memory)
# print(output)


def train(inputs, outputs, rules, examples):
	scores = Dict()
	for i in outputs:
		scores[i] = 0

	for i in range(len(examples)):
		values = examples[i]
		total = sum(list(values.values()))

		for j in range(len(rules)):
			function = convert(rules[j])
			score = function(values)
			index = outputs[j]
			scores[j] += score * 1/len(examples)
	return scores


# rules = []

# inputs  = [0,1,2]
# outputs = []

# examples = []
# for i in range(10):
# 	example = Dict()
# 	for j in range(len(inputs)):
# 		example[j] = 0
# 	for j in range(2):
# 		example[rr(len(example))] = 1
# 	examples.append(example)

# 	active = [rr(len(inputs)) for j in range(2)]
# 	rules.append(create('conjunction', active))
# 	outputs.append(i)

# y = train(inputs, outputs, rules, examples)
# print(y)