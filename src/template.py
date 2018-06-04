from lib.functions import *
from lib.relations import *
from lib.constraints import *
from lib.util import *

def product(X):
	y = X[0]
	for i in range(1, len(X)):
		y *= X[i]
	return y

def is_template(object):
	return isinstance(object, Dict) and equivalent(object.keys(), ['type', 'data'])

def template(type=None, data=None):
	return Dict({'type':type, 'data':data})

def association(group=None):
	output = template('association')
	output['group'] = group
	return output

def implication(premise=None, conclusion=None):
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
	if type == 'association':
		return Association(data)
	if type == 'implication':
		return Implication(data[0], data[1])

class Proposition:
	def __call__(self, memory):
		return

class Truth(Proposition):
	def __init__(self, variable):
		self.variable = variable
	def __call__(self, memory):
		return self.variable in memory.keys() and memory[self.variable] == 1

class Implication(Proposition):
	def __init__(self, premise, conclusion):
		self.premise = premise
		self.conclusion = conclusion
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

class Association(Proposition):
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
		string += str(premise) + ' / ' + str(conclusion)

	elif isinstance(proposition, Association):
		group = proposition.group
		if isinstance(group[0], Proposition):
			group[0] = express(group[0], '')
		string += str(group[0])
		for i in range(1, len(group)):
			string += ' ^ '
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
	def __init__(self):
		super().__init__(0)
		self.state = 0

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
	else:
		a,r,b = tree
		if r == '^':
			r = 'association'
		if r == '/':
			r = 'implication'
		x = [a, b]
		return template(r, x)

def generate(expression):
	tree = ExpressionTree()
	tree.parse(expression)
	template = encode(tree)
	function = convert(template)
	return function