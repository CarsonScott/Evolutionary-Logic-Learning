from pattern_memory import *
from probability_distribution import *
from function import *

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

class Operation(PatternMemory):
	def __init__(self, function, *input):
		super().__init__()
		k = str(function.__name__)
		self[k] = function 
		self.function = k
		self.input = Matrix()
		K = Matrix(i for i in range(len(X)))
		for k in range(len(K)):
			self[k] = K[k]
			self.input.append(k)

	def identify(self, index):
		if index in self.keys():
			return 'key'
		elif identify(index) == 'matrix':
			return 'pattern'
		return super().identify(index)
	def get_function(self):
		return self.translate(self.function)
	def get_input(self):
		return self.translate(self.input)
	def __call__(self):
		f = self.get_function()
		X = self.get_input()
		if iterable(X) and len(X) == 1:
			X = self.translate(X[0])
			return call(X[0], *X[1:])
		F = associate(*to_matrix(f, *X))
		if len(X) == 1:
			X = self.translate(X[0])
		if not iterable(X) or iterable(X) and len(X) == 0:
			Y = F
		elif iterable(X):
			Y = f(X)
		else:
			Y = f(X)
		return Y

class WordResponder(Function):
	def __init__(self, words, operations):
		super().__init__(create(markers, operations))

class WordClassifier(Function):
	def __init__(self, valid, marker, ignore):
		super().__init__()
		for w in valid:
			self.set(w, 'valid')
		for w in marker:
			self.set(w, 'marker')

		for w in ignore:
			self.set(w, 'ignore')
		self.set(None, 'ignore')

# f1 = WordClassifier('abcdefghijklmnopqrstuvwxyz0123456789', '|-.', ' ')

# print(f1('a'), f1('.'), f1(' '))

# class FunctionMemory(PatternMemory): 
# 	def construct(self, instructions):
# 		for x in instructions:
# 	#	Grammar

# 		#	word marker
# 			if x == '-':
# 				pass
# 		#	phrase marker
# 			elif x == ' ':
# 				pass

# 		#	sentence marker
# 			if x == ';':
# 				pass

# 			elif x in self.keys():
# 				pass

# 		#	Semantics
		
# 			#	world value
# 			if x in self.keys():
# 				pass
# 			#	phrase value
		
# 			# 	setence value


space = AssociativeMemory([str(i) for i in range(15)], 10)
keys = space.keys()

options = Matrix(keys)
pattern = []

for i in range(15):
	x = options[rr(len(options))]
	del options[options.index(x)]
	pattern.append(x)

print(pattern)
p = 0
string = ''
count = 0
log = open("log.txt", 'w')
for i in range(1000):
	x = pattern[p]
	p += 1
	if p == len(pattern):
		p = 0
	space.append(x)
	if i % 10 == 0:
		for j in range(len(keys)):
			k1 = keys[j]
			value = space.compute(k1)
			utilities = space.update()

		count += 1
		utilities = space.update()
		string += str(count) + '	'
		for k in keys:
			string += str(utilities[k]) + '	'
		print(string)
		log.write(string + '\n')
log.close()

		
# for x in keys:

# if __name__ == "__main__":
# 	agent = Agent()
# 	agent['a'] = 1
# 	agent['b'] = 1
# 	agent['c'] = agent.construct('+', 'a', 'b')

# 	y = agent.construct('+', 'a', 'b')
# 	print(agent.generate('(a ^ b);'))
# 	# print(is_template(y))
# 	# class FunctionMemory(PatternMemory):
# 	# 	def construct(self, data):
# 	# 		data = self.translate(data)
# 	# 		model = Model(data)
# 	# 		return model

# 	# 	def identify(self, data):
# 	# 		if isinstance(data, Model):
# 	# 			return 'model'
# 	# 		return super().identify(data)

# 	# 	def convert(self, key):
# 	# 		self[key] = self.construct(key)

# 	# 	def __call__(self, data):
# 	# 		if self.identify(self.translate(data)) == 'pattern':
# 	# 			data = self.translate(data)
# 	# 			if self.identify(self.translate(data[0])) == 'model':
# 	# 				f = self[data[0]].get_function()
# 	# 				f = self.translate(data[0]).get_function()
# 	# 				x = self.translate(data[0]).get_inputs()
# 	# 				data = tuple([f] + x)
# 	# tuple([f] + x)		return super().__call__(data)
		

# 	# mem = FunctionMemory()
# 	# mem['a'] = ('^', 'b', 'c')
# 	# mem['b'] = 5
# 	# mem['c'] = 3
# 	# mem['d'] = 3
# 	# mem.convert('a')

# 	# y = mem(('a', 'b', 'd'))
# 	# print(y)
