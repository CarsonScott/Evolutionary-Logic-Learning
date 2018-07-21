from lib.util import *
from lib.template import *
from matrix import *

_OPEN = '('
_CLOSE = ')'
_SPACE = ' '
_BREAK = ';'

def classify(x):
	if callable(x):
		return 'function'
	elif x == _OPEN:
		return '_open'
	elif x == _CLOSE:
		return '_close'
	elif x == _SPACE:
		return '_space'
	elif x == _BREAK:
		return '_break'
	return 'data'

def is_statement(x):
	pattern = execute(classify, x)
	return pattern == ['data', 'function', 'data']

def create_statement(x, R, y):
	function = Dictionary()
	function + ('relation', R)
	function + ('inputs', [x, y])
	return function

class ProcessLanguage(Dictionary):
	
	def __setitem__(self, K, X):
		if iterable(K):
			for i in range(len(K)):
				self[K[i]] = X[i]
		else:super().__setitem__(K, X)
	def __call__(self, data):
		tree = self.parse(data)
		model = self.convert(tree)
		return self.execute(model)

	def translate(self, X):
		Y = X
		if iterable(X):Y = execute(self.translate, X)
		elif X in self:Y = self.translate(self[X])
		return Y

	def extract(self, X):
		Y = []
		for i in range(1, len(X)-1, 1):
			x = self.translate(X[i-1:i+2])
			if is_statement(x):
				Y.append(x)
		return Y

	def convert(self, X):
		Y = X
		x = X
		if isinstance(X, Dictionary) == False:
			if is_statement(x):
				Y = create_statement(*x)
			else:
				Y = x
				for j in range(len(x)):
					if iterable(x[j]) and is_statement(x[j]):
						Y[j] = create_statement(*x[j])
		return Y

	def execute(self, X):
		Y = X
		if isinstance(X, Dictionary):
			f = X['relation']
			x = X['inputs']
			for i in range(len(x)):
				if isinstance(x[i], Dictionary):
					x[i] = self.convert(x[i])
			Y = f(x)
		else:
			if iterable(X):
				if is_statement(X):
					Y = self.convert(X)
				else:
					for i in range(len(X)):
						Y[i] = self.convert(X[i])
		return Y

	def parse(self, X):
		statement = X + ' '
		structure = []
		outputs = []
		string = ''
		for c in statement:
			X = structure[len(structure)-3:len(structure)]
			print(X)
			if len(X) >= 3:
				if is_statement(X):
					function = create_statement(*X)
					structure = [function]
				else:structure = []
			if c == ' ':
				if string != '':
					if string in self:
						structure.append(self.translate(string))
					else:
						try:
							if int(string) == float(string):
								structure.append(int(string))
							else:structure.append(float(string))
						except:structure.append(string)
					string = ''
			else:string += c
		return structure

def POW(X):return X[0] ** X[1]
def LEN(X):return len(X)

memory = ProcessLanguage()
memory['a b c d e f'.split(' ')] = (True, True, False, 2, 43, [2, 3])
memory['+ - * / ^ and or not'.split(' ')] = (ADD, SUB, MULT, DIV, POW, AND, OR, NOT)
statement = 'a and b or c'
