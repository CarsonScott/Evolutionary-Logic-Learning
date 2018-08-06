from function_language import *

class Topology(Function):
	def __init__(self, objects=[]):
		super().__init__()
		self.set_dependent('objects', [])
		self.set_dependent('functions', [])
		for i in objects:
			self.set_object(i)

	def set_object(self, key, sources=[], targets=[]):
		self['.objects'].append(key)
		self.set_sources(key, sources)
		self.set_targets(key, targets)

	def set_path(self, source, target):
		path = (source, target)
		key = merge('.', list(path))
		self.set_target(source, target)
		self.set_source(target, source)

	def set_source(self, key, source=None):
		if not self.has(str(key) + '.sources'):
			self.set_dependent(key, 'sources', [])
		if source != None:self[str(key) + '.sources'].append(source)

	def set_target(self, key, target=None):
		if not self.has(str(key) + '.targets'):
			self.set_dependent(key, 'targets', [])
		if target != None:
			self[str(key) + '.targets'].append(target)

	def set_function(self, key, function):
		self.set_dependent('functions', key, function)

	def get_function(self, key):
		self.get_dependent('functions', key)

	def get_objects(self):
		return self.get_dependent('objects')

	def set_objects(self, objects, values=None):
		self.set_dependent('objects', objects)
		for i in range(len(objects)):
			x = None
			if values != None:
				x = values[i]
			self[objects[i]] = x
	def get_sources(self, key):
		return self.get_dependent(key, 'sources')

	def set_sources(self, key, sources):
		for source in sources:
			self.set_source(key, source)

	def get_targets(self, key):
		return self.get_dependent(key, 'targets')

	def set_targets(self, key, targets):
		for target in targets:
			self.set_target(key, target)

	def get_reachable(self, key, depth=None, visited=None):
		root = False
		if visited == None: 
			root = True
			visited = []

		reachable = [key]
		visited.append(key)
		if depth != None: depth -= 1		
		if depth == None or depth >= 0:
			reachable = compliment(visited, self.get_targets(key))
			for i in reachable:
				R, V = self.get_reachable(i, depth, visited)
				reachable = union(reachable, R)
				visited = union(visited, V)
		if root: return reachable
		return reachable, visited

	def set_statement(self, statement):
		self['.statements'].append(statement)
	
	def get_statements(self):
		return self.get_dependent('statements')
	
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
	
	def execute(self, function):
		if self.has(function):
			function = self[function]
		return super().execute(function)

	