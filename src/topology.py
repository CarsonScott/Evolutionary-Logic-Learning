from function_language import *

class Topology(Function):
	def __init__(self, objects=[]):
		super().__init__()
		self.set_dependent('objects', [])
		self.set_dependent('functions', [])
		self.set_features(['sources', 'targets'])
		for i in objects:
			self.set_object(i)

	def set_object(self, key, sources=[], targets=[]):
		self['.objects'].append(key)
		self['value'][key] = key
		self['sources'][key] = []
		self['targets'][key] = []
		# self.set(key, {'sources':sources, 'targets':targets})
		# self.set_sources(key, sources)
		# self.set_targets(key, targets)

	def set_path(self, *keys):
		for i in range(1, len(keys)):
			source = keys[i-1]
			target = keys[i]
			if self['sources'][target] == None:
				self['sources'][target] = []
			elif source not in self['sources'][target]:
				self['sources'][target].append(source)
			
			if self['targets'][source] == None:
				self['targets'][source] = []
			elif target not in self['targets'][source]:
				self['targets'][source].append(target)
		# self.set_source(target, source)
		# self.set_target(source, target)
		# self['sources'][target].append(source)
		# self['targets'][source].append(target)
		# self.set_target(source, target)
		# self.set_source(target, source)

	def set_source(self, key, source=None):
		if not key in self['.objects']:
			self.set_object(key)
		if str(key) not in self['sources'].keys():
			self['sources'][str(key)] = []
		if source != None:
			if source not in self['sources'][str(key)]:
				self['sources'][str(key)].append(source)

	def set_target(self, key, target=None):
		if not key in self.get_dependent('objects'):
			self.set_object(key)
		if str(key) not in self['targets'].keys():
			self['targets'][str(key)] = []
		if target != None:
			if target not in self['targets'][str(key)]:
				self['targets'][str(key)].append(target)

	def set_function(self, key, function):
		self.set_dependent('functions', key, function)

	def get_function(self, key):
		self.get_dependent('functions', key)

	def get_objects(self):
		return self.get_dependent('objects')

	# def set_objects(self, objects, values=None):
		# self.set_dependent('objects', objects)
		# for i in range(len(objects)):
		# 	self.set_object(objects[i], va)
		# 	x = None
		# 	if values != None:
		# 		x = values[i]
		# 	self[objects[i]] = x

	def get_sources(self, key):
		return self['sources'][key]
		# if str(key) in self['sources'].keys():	
		# 	# return self.get_dependent('sources', key)
		# return []

	def set_sources(self, key, sources):
		self['sources'][key] = sources
		# for source in sources:
		# 	self.set_source(key, source)

	def get_targets(self, key):
		return self['targets'][key]
		# if str(key) in self['targets'].keys():
		# 	return self['targets'][str(key)]
		# 	# return self.get_dependent('targets', key)
		# return []

	def set_targets(self, key, targets):
		for target in targets:
			self.set_target(key, target)

	def get_reachable(self, key, depth=None, visited=None):
		initial = False
		if visited == None: 
			initial = True
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
		if initial: return reachable
		return reachable, visited

	def get_interface(self):
		keys = self.get_objects()
		inputs = []
		outputs = []
		disjoint = []
		for i in keys:
			sources = self.get_sources(i)
			targets = self.get_targets(i)

			x, y = sources == [], targets == []
			if x and y:
				disjoint.append(i)
			elif x:
				inputs.append(i)
			elif y:
				outputs.append(i)

		return inputs,outputs,disjoint

	def set_statement(self, statement):
		self['.statements'].append(statement)
	
	def get_statements(self):
		return self.get_dependent('statements')
	
	def get_outputs(self):
		return self.get_dependent('outputs')
		# return [self[i] for i in outputs]

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

	