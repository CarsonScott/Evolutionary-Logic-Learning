from matrix import *
from Generator import *

class Structure(Memory):
	def __init__(self, type=None):
		super().__init__()
		self['type'] = type

class System(Structure):
	def __init__(self, ):
		super().__init__('agent')

def Function(x_type=None, y_type=None):
	structure =  Structure('function')
	structure['x_type'] = x_type
	structure['y_type'] = y_type

# def evaluate(structure):
# 	if structure['type'] == 'function':



# M = Matrix([2,[2, [3, 5]], 3])
# S = get_shape(M)
# print(M, S)


def construction(group=None):
	return template('construction', group)

class Construction(Proposition):
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


# G2 = Generator(5, f1)
# for i in range(1000):
# 	print(G2(i))
# g = FunctionGenerator(2)
# g['and'] = AND
# g['x'] = True
# g['y'] = False
# g['a'] = False
# g['b'] = False
 
# X = ['and', 'x', 'y', 'and', 'a', 'b']
# for i in range(len(X)):
# 	f = g(X[i])
# print(g['data'])