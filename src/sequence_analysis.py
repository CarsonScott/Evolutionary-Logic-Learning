from lib.util import *
from lib.data import *
from functional_neural_network import *

filenames = get_filenames('functions')

for fn in filenames:
	function = load('functions/' + fn)
	inputs = []
	functions = []
	for i in function.keys():
		x = function.get_inputs(i)
		if x != None:
			inputs = union(inputs, x)
		else:
			inputs.append(x)
		functions.append(function.get_function(i)) #= union(functions, function.get_inputs(i))
	function.set_values(function.keys(), [unknown for i in function.keys()])
	# function = FunctionalTopology(inputs, function.get_capacity(), functions)
	function.init(function.get_capacity())
	observations = []
	input_size = len(function.get_leaves())
	inputs = []
	for i in range(input_size):
		inputs.append(rr(2))
	function.inputs(inputs)
	limit = 10000
	for count in range(10000):
		function.update()
		print(function.get_values(function.keys()))
		# if count < limit-1:
		# 	print(count, '	', merge(',',f.get_history()))# + '	' + str(unknown not in network.outputs()))
			# save(f, 'functions/' + random_str(5) + '.bin')
	# if count < limit:
		# observations.append(network.get_history())
		# print(network.get_history())


# class Analysis:
# 	def __init__(self, symbols, size):
# 		self.symbols = symbols
# 		self.capacity = size
# 		self.sequence = []
# 		self.step = 0
# 		self.probabilities = list([0 for i in symbols])
# 	def update_probability(self, symbol, increment=1):
# 		self.probabilities[symbol] += 1
# 	def set_value(self, symbol):
# 		if symbol in self.symbols:
# 			self.sequence.append([value])

# 		if len(self.sequence) > self.capacity:
# 			sort(self.probabilities)