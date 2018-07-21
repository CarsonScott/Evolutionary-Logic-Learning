from lib.util import *

class FunctionWord:
	def __init__(self, word, rules):
		self.word = word
		self.rules = rules

	def __gt__(self, other):
		if identify(other) == 'functionword':
			other = other.word
		if self.word in self.rules.keys():
			if other in self.rules[self.word]:
				return True
		else:return False
		
		if other in self.rules.keys():
			if self.word in self.rules[other]:
				return False
		else:return True

	def __lt__(self, other):
		gt = self.__gt__(other)
		if gt != None:
			return not gt

rules = Dict({'*':['+'],
})

w1 = FunctionWord('*', rules)
w2 = FunctionWord('+', rules)

class Language(Dict):
	def __init__(self, rules):
		self.rules = rules
		self.statement = []

	def set_rule(self, word1, word2):
		if word1 not in self.rules:
			self.rules[word1] = [word2]
		elif word2 not in self.rules:
			self.rules[word1].append(word2)

	def compare(self, word1, word2):
		if self.get_type(word1) == 'function' and self.get_type(word2) == 'function':
			return self[word1] > self[word2]

	def set_word(self, word, type='content'):
		if type == 'content':
			self[word] = None
		elif type == 'function':
			self[word] = FunctionWord(word, self.rules)

	def get_type(self, word):
		if self[word] == None:
			return 'content'
		elif identify(self[word]) == 'functionword':
			return 'function'

	def update(self, word):
		self.statement.append(word)

	def analyze(self, statement):
		output = []
		for word in statement:
			output.append(self.get_type(word))

		functions = []
		comparisons = []
		previous_function = None
		for i in range(len(output)):
			t = output[i]
			w = statement[i]
			if t == 'function':
				if len(functions) == 0:
					comparisons.append(True)
				else:
					comparisons.append(self.compare(w, previous_function))
				previous_function = w
				functions.append(i)

		previous_model = []
		for i in range(len(functions)):
			j = functions[i]
			model = [j-1, j, j+1]

		print(functions)
		print(comparisons)

language = Language(rules)
language.set_rule('*', '+')


language.set_word('a')
language.set_word('b')
language.set_word('c')
language.set_word('+', 'function')
language.set_word('*', 'function')

language.analyze(['a', '+', 'b', '*', 'c'])
