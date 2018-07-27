from lib.functions import *
from lib.relations import *
from lib.constraints import *
from lib.util import *
from template import *

class EmbeddedList(list):
	def __init__(self, size, value=None):
		for i in range(size):
			self.append(value)
	def expand(self, index):
		self[index] = EmbeddedList(1, self[index])
	def reduce(self, index):

GRAMMAR_SYMBOLS = ['(', ')', ';', ' ']
CONNECTIVE_SYMBOLS = ['^', '|', '<']
CONNECTIVE_NAMES = ['conjunction', 'disjunction', 'implication']
CONNECTIVE_FUNCTIONS = [Conjunction, Disjunction, Implication]

class Language(Dict):
	def __init__(self):
		self.functions = Dict()
		self.grammar = list()
		self.names = Dict()
	def set_object(self, symbol, function, name=None):
		self.functions[symbol] = function
		if name != None or symbol not in self.names.keys():
			self.names[symbol] = name
	def get_function(self, symbol):
		if self.contains(symbol):
			function = self.functions[symbol]
			return function
	def get_name(self, symbol):
		if self.contains(symbol):
			name = self.names[symbol]
			return name
	def get_object(self, symbol):
		if self.contains(symbol):
			return self.get_function(symbol), self.get_name(symbol)
	def contains(self, symbol):
		return symbol in self.functions.keys() and symbol in self.names.keys() and symbol not in self.grammar

class ExpressionTree(EmbeddedList):
	def __init__(self, language=None):
		super().__init__(0)
		self.state = 0
		self.functions = Dict()
		self.language = language
		
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
			if not self.language.contains(character):
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

	def encode(self):
		for i in range(len(self)):
			if isinstance(self[i], ExpressionTree):
				self[i] = encode(self[i])
		if len(self) == 1:
			return self[0]
		elif len(self) == 3:
			a,f,b = self
			f = self.language.get_name(f)
			x = [a,b]
			return template(f, x)
	def convert(self, template):
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

		if self.language.contains(type):
			return self.language.functions[type]# CONNECTIVE_FUNCTIONS[index](data)
	def generate(self, expression):
		tree = ExpressionTree()
		tree.parse(expression)
		template = self.encode(tree)
		function = self.convert(template)
		return function

	def variables(self, expression):
		tree = ExpressionTree()
		tree.parse(expression)
		print(tree)

	def express(self, proposition, marker=';'):
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

			index = self.functions.index(Implication)
			symbol = self.function_symbols[index]
			string += str(premise) + ' ' + symbol + ' ' + str(conclusion)

		elif isinstance(proposition, Conjunction):
			group = proposition.group
			if isinstance(group[0], Proposition):
				group[0] = express(group[0], '')
			string += str(group[0])

			index = self.functions.index(Conjunction)
			symbol = self.function_symbols[index]
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
			index = self.functions.index(Disjunction)
			symbol = self.function_symbols[index]
			for i in range(1, len(group)):
				string += ' ' + symbol + ' '
				data = group[i]
				if isinstance(data, Proposition):
					data = express(data, '')
				string += str(data)
		return string + ')' + marker

tree=ExpressionTree()