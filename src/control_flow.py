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
	
	def __init__(self, function=random_choice):
		super().__init__()
		self.set_dependent('function', function)
		self.set_dependent('outputs', list())
		self.set_dependent('inputs', list())
		self.set_dependent('options', list())
		self.set_dependent('state', None)
		self['inputs'] = ['.inputs', '.options']

	# # def __getitem__(self, key):
	# # 	if '.' in key:
	# # 		# a,b = key.split('.')
	# # 		print(a,b)
	# # 		if a != '':
	# # 			return self.get_dependent(a,b)
	# 		else:
	# 			return self.get_dependent(a)
	# 	return super().__getitem__(key)
	def get_state(self):
		return self.get_dependent('state')

	def set_state(self, state):
		self.set_dependent('state', state)

	def get_options(self, state):
		return self.get_targets(state)

	def set_options(self, options):
		self['.options'] = options

	def get_statements(self):
		return self.get_dependent('statements')

	def set_statements(self, statements):
		return self.set_dependent('statements', statements)
	
	def get_outputs(self):
		outputs = self.get_dependent('outputs')
		return self.get_values(outputs)

	def set_outputs(self, outputs):
		return self.set_dependent('outputs', outputs)

	def get_inputs(self):
		return self.get_dependent('inputs')

	def set_inputs(self, inputs):
		self.set_dependent('inputs', inputs)

	def compile_inputs(self):
		keys = self.get_inputs()
		values = []
		for i in keys:
			values.append(self[i])
		return values

	def compile_options(self):
		state = self.get_state()
		options = self.get_options(state)
		index = 0
		values = []
		for i in options:	
			values.append(options[index])
			index += 1
		return values

	def compile_outputs(self):
		keys = self.get_outputs()
		values = []
		for i in keys:
			value = self[i]
			values.append(value)
		return values

	def store_inputs(self, inputs):
		keys = self.get_inputs()
		index = 0
		for i in keys:	
			self[i] = inputs[index]
			index += 1

	def update(self, inputs):
		self.store_inputs(inputs)
		inputs = [self.compile_inputs(), self.compile_options()]
		super().update(inputs)
	
	def execute(self, function):
		if self.has(function):
			function = self[function]
		return super().execute(function)

	def compute(self):
		statements = self.get_statements()
		self.set_options(self.get_options(self.get_state()))
		for statement in statements:
			self['template'] = create_template(statement)
			super().compute()
		outputs = self.compile_outputs()
		return outputs

	def __call__(self, inputs=[]):
		self.update(inputs)
		return self.compute()
			
ps = PathSelector(random_choice)
keys = 'a b c d y a j k'.split()

ps.set_objects(keys, keys)
ps.set_path('a','b')
ps.set_path('a','j')
ps.set_path('j','k')
ps.set_path('k','d')
ps.set_path('b','c')
ps.set_path('c','d')
ps.set_path('d','y')
ps.set_path('y','a')

statements = ['.state = .function(.options)']

ps.set_outputs(['.state'])
ps.set_statements(statements)

sequence = []
initial = 'b'

ps.set_state(initial)
for i in range(100):
	state = ps([])
	print(state)