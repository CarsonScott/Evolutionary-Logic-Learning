from matrix import *
from lib.util import Dict
from pattern_memory import *

def all_equal(X):
	s = len(X[0])
	for x in X:
		if len(x) != s:
			return False
		s = len(x)
	return True

class FunctionMemory(PatternMemory):
	def __init__(self, function=None):
		super().__init__()
		self.inputs = []
		self.outputs = []
		self.function = function

	def identify(self, value):
		if identify(value) == 'matrix':
			return 'matrix'
		if identify(value) == 'data':
			return 'data'
		return super().identify(value)

	def create_transformation(self, key, inputs, functions, weights):
		self[key] = Matrix([inputs, functions, weights])

	def set_function(self, key, function, input_type, output_type):
		self[key] = [function, input_type, output_type]
		self.functions.append(key)

	def set_input(self, key):
		self[key] = None
		self.inputs.append(key)

def id(x):
	return x

# fm = FunctionMemory()
# keys = []
# for i in range(10):
# 	fm[str(i)] = rr(10)/10
# 	keys.append(str(i))

# class Data(Matrix):
# 	pass

# fm['all_variables'] = tuple(['mat'] + keys)
# fm['dat'] = Data
# fm['list'] = list
# fm['in'] = In
# fm['threshold'] = 0.5
# fm['f'] = ('<', 'threshold', 'all_variables')

# print(fm('f'))
# # fm['t1'] = Matrix([['a', ('+', 'b', 'c')], [0.5, 0.5, 0.5]])
# # fm.function = 't1'
# # y = fm()

# # print(y)*