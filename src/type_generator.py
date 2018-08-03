from dictionary import *
from lib.relations import *

def equivalence(X,Y):
	Z = []
	for i in range(len(X)):
		Z.append(X[i] == Y[i])
	return Z
def difference(X,Y):
	Z = []
	for i in range(len(X)):
		Z.append(X[i] - Y[i])
	return Z

def conjunction(X):
	return False not in X
def disjunction(X):
	return True in X

def apply_functions(x, F):
	Y = []
	for f in F:
		Y.append(f(x))
	return Y

class TypeGenerator(Dictionary):
	def __init__(self, objects, functions=None):
		self['objects'] = objects
		self['functions'] = functions
		self['comparison'] = equivalence
		self['decision'] = conjunction
		self['learning'] = True

	def __getitem__(self, key):
		if isinstance(key, tuple):
			if len(key) == 2:
				if isinstance(key[0], int):
					if isinstance(key[1], int):
						if key[0] > key[1]:
							key = key[1], key[0]
						return super().__getitem__(key)
		else:
			return super().__getitem__(key)

	def get_equal(self, index):
		equal = []
		for i in range(len(self['objects'])):
			if i not in equal:
				if i == index:
					equal.append(i)
				else:
					key = (index, i)
					if i < index:
						key = (i, index)
					if key not in self.keys():
						equal.append(i)
					elif self[key]:
						equal.append(i)
		return equal

	def get_groups(self):
		if 'groups' not in self.keys():
			groups = []
			stored = []
			for i in range(len(self['objects'])):
				if i not in stored:
					equal = self.get_equal(i)
					assignment = None
					for j in range(len(groups)):
						if not disjoint(equal, groups[j]):
							assignment = j
							break
					if assignment == None:
						groups.append(equal)
						stored.append(len(groups)-1)
					elif i not in groups[assignment]:
						groups[j].append(i)
						stored.append(i)
			self['groups'] = groups
		return self['groups']

	def get_models(self):
		if 'models' not in self.keys():
			groups = self.get_groups()
			models = []	
			functions = self['functions']
			for i in range(len(groups)):
				model = []
				index = groups[i][0]
				object = self['objects'][index]
				if functions == None:
					model = object
				else:
					for function in functions:
						model.append(function(object))
				models.append(model)
			self['models'] = models
		return self['models']

	def compute(self, index1, index2):
		object1 = self['objects'][index1]
		object2 = self['objects'][index2]
		model1 = []
		model2 = []

		functions = self['functions']
		if functions == None:
			model1 = object1
			model2 = object2
		else:
			for function in functions:
				output1 = function(object1)
				output2 = function(object2)
				model1.append(output1)
				model2.append(output2)
		comparison = self['comparison'](model1, model2)
		decision = self['decision'](comparison)
		
		key = (index1, index2)
		if index1 > index2:
			key = (index2, index1)
		self[key] = decision
		
	def generate(self):
		objects = self['objects']
		for i in range(len(objects)):
			for j in range(i, len(objects)):
				if i != j:
					self.compute(i,j)
		return self.get_models()

	def __call__(self, x):
		x = apply_functions(x, self['functions'])
		models = self.get_models()
		groups = self.get_groups()
		for i in range(len(models)):
			model = models[i]
			if model == x:
				return i
		if self['learning']:
			self['groups'].append(x)
			self['models'].append(x)
			return len(self['groups'])-1


def f1(x):
	return isinstance(x, int)
def f2(x):
	return isinstance(x, bool)
def f3(x):
	return x == None
def f4(x):
	return isinstance(x, list)
def f5(x):
	return 'a' in str(x)
def f6(x):
	if f1(x):
		return x >= 0

def RAND():
	value = None
	x = rr(4)
	if x == 0:
		value = rr(-10, 10) 
	if x == 1:
		value = random_str(10)
	if x == 2:
		value = bool(rr(2))
	if rr(1000) < 4:
		value = [RAND() for i in range(rr(10))]
	return value

objects = [RAND() for i in range(100)]
functions = [f1, f2, f3, f4, f5, f6]

generator = TypeGenerator(objects, functions)
models = generator.generate()

examples = [RAND() for i in range(25)]
types = [generator(x) for x in examples]
print(types)