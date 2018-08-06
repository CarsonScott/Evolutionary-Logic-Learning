from topology import *

def random_choice(X):
	return X[rr(len(X))]

def preferred_choice(X):
	if iterable(X):
		if 'a' in X:
			return 'a'
		if 'b' in X:
			return 'b'
		return random_choice(X)

class PathSelector(Topology):
	
	def __init__(self):
		super().__init__()
		self.set_dependent('function')
		self.set_dependent('options')
		self.set_dependent('state')
		self.set_dependent('inputs', [])
		self.set_dependent('outputs', ['.state'])
		self.set_dependent('statements', ['.state = .function(.options)'])

	def set_state(self, state):
		self.set_dependent('state', state)
	def set_function(self, function):
		self.set_dependent('function', function)

	def get_options(self):
		return self.get_targets(self.get_dependent('state'))
	def set_options(self, options):
		return self.set_dependent('options', options)
	def compile_options(self):
		state = self.get_state()
		options = self.get_options(state)
		index = 0
		values = []
		for i in options:	
			values.append(options[index])
			index += 1
		return values

	def assign(self):
		options = self.get_options()
		self.set_options(options)

	def compute(self):
		statements = self.get_statements()
		for i in range(len(statements)):
			statement = statements[i]
			if isinstance(statement, str):
				self['.statements'][i] = create_template(statement)
				statement = self['.statements'][i]
			self.set_dependent('template', statement)
			super().compute()
		return self.compile_outputs()

	def __call__(self, inputs=[]):
		self.assign()
		self.update(inputs)
		return self.compute()

# keys = 'a b c d y a j k'.split()

# ps = PathSelector()
# ps.set_function(random_choice)
# ps.set_objects(keys, keys)
# ps.set_path('a','b')
# ps.set_path('a','j')
# ps.set_path('j','k')
# ps.set_path('k','d')
# ps.set_path('b','c')
# ps.set_path('c','d')
# ps.set_path('d','y')
# ps.set_path('y','a')


# outputs = []
# initial = 'a'
# ps.set_state(initial)
# for i in range(100):
# 	state = ps()
# 	outputs.append(state)
# print(outputs)