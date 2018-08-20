from functional_memory import *

class Unknown(object):
	def __repr__(self):
		return 'unknown'

class Map(Template):
	def map(self, x, y):
		if x in self.keys():
			if isinstance(self[x], list): 
				if y not in self[x]:
					self[x].append(y)
			else:
				if y != self[x]:
					self[x] = [self[x], y]
		else:self[x] = y
	def __call__(self, x):
		if x in self.keys():
			return self[x]
		else:return Unknown()

# m = Map()
# m.map(3, 1)
# m.map(3, 2)

# def add(x,y):
# 	return x+y
# def mult(x,y):
# 	return x*y
# def div(x,y):
# 	return float(x/y)
# def sub(x,y):
# 	return x-y

# memory = Memory()
# memory.set('x', 10, 'y', 3, 'function', Function, 'int', int, 'float', float, 'str', str, 'list', list)

# # Base functions
# memory.compose('f', [f, 'int', 'int'])
# memory.compose('g', [g, 'int', 'str'])
# memory.compose('h', [h, 'str', 'int'])
# memory.compose('add', [add, ['int', 'int'], 'int'])
# memory.compose('sub', [sub, ['int', 'int'], 'int'])
# memory.compose('mult', [mult, ['int', 'int'], 'int'])
# memory.compose('div', [div, ['int', 'int'], 'float'])

# # Composite functions
# memory.compose('h', ['f', 'g'])

# # Sequence function
# memory.set('seq', ['add', 'mult', 'div', 'sub'])

# # Function outputs
# print(memory.compute('add', Collection(['x', 'y'])))
# print(memory.compute('mult', Collection(['x', 'y'])))
# print(memory.compute('div', Collection(['x', 'y'])))
# print(memory.compute('sub', Collection(['x', 'y'])))
# print(memory.compute('seq', Collection(['x', 'y'])))
# print(memory.compute('h', 1))
# print(memory.compute('tree', 'add'))


# memory.compose('f.g', ['f', 'g'])
# memory.compose('f.f.g', ['f', 'f.g'])
# y = memory.compute('t', 'f.f.g')
# print(y)

# t = retrieve(memory['f.g'].tree(), 'input')
# t = retrieve(memory['f.g'].tree(), 'output')
# print(t)
# class RelationMemory(MemorySpace):
# 	def __init__(self):
# 		super().__init__(['input', 
# 						  'variable', 
# 						  'output', 
# 						  'function', 
# 						  'operation', 
# 						  'model', 
# 						  'model'], 
# 						  [])
# 		self.outputs = MemorySpace()
# 	def compute(self, data):
# 		if isinstance(data, str):
# 			if data in self.keys():
# 				data = self[data]
# 		output = data
# 		if isinstance(data, Schema):
# 			function_keys = 'function input output'.split()
# 			model_keys = 'input output'.split()
	
# 			if contains(data.keys(), function_keys):
# 				function = data['function']
# 				inputs = data['input']
# 				outputs = data['output']
# 				function = self.compute(function)
# 				inputs = self.compute(inputs)
# 				output = function(inputs)
# 				if not isinstance(outputs, list):
# 					outputs = [outputs]
# 				if isinstance(outputs, list):
# 					for i in outputs:
# 						if i in self:
# 							if isinstance(output, list) and len(output) < outputs.index(i):
# 								self[i] = output[outputs.index(i)]
# 							else:self[i] = output

# 			elif contains(data.keys(), model_keys):
# 				inputs = data['input']
# 				outputs = data['output']
# 				X = self.compute(self[inputs]['input'])
# 				inputs = self.compute(inputs)
# 				outputs = self.compute(inputs)
# 				output = X,outputs

# 		elif isinstance(data, list):
# 			output = list() 
# 			for i in range(len(data)):
# 				output.append(self.compute(data[i]))
# 		elif isinstance(output, str):
# 			return self.compute(output)
# 		return output
# 	def clear_outputs(self, keys=None):
# 		if keys == None:
# 			keys = self.outputs.keys()
# 		for i in keys:
# 			if i in self.outputs.keys():
# 				del self.outputs[i]
# 	def get_values(self, keys):
# 		values = []
# 		for i in keys:
# 			if i not in self.outputs.keys() or self.outputs[i] == None:
# 				x = self[i]
# 			else:x = self.outputs[i]
# 			values.append(x)
# 		return values
# 	def get_class(self, key):
# 		keys = self.classes[key]
# 		return self.get_values(keys)
# 	def update_variable(self, key, value=None):
# 		data = key
# 		if isinstance(key, str) and key in self.keys():
# 			data = self[key]
# 		classes = self.get_classes(data)
# 		if classes != None:
# 			if 'operator' in classes:
# 				value = self.compute(data)
# 				key = self[key]['function'] + '('
# 				key += merge(',',data['input']) + ')'
# 				self.set_classes(key, 'output')
# 				self[key] = value
# 			elif 'model' in classes:
# 				value = self.compute(data)
# 				self[key] = value
# 				self.outputs[key] = value
# 			if value != None:
# 				self[key] = value
# 				self.outputs[key] = value
# 	def update_variables(self, keys=[], values=[]):
# 		for i in range(len(keys)):
# 			self.outputs[keys[i]] = None
# 			self.update_variable(keys[i], values[i])
# 	def update_class(self, key, values=[]):
# 		keys = self.classes[key]
# 		self.update_variables(keys, values)
# 	def __call__(self, values=[]):
# 		self.clear_outputs(self.classes['output'])
# 		self.update_class('input', values)
# 		self.update_class('output', [None for i in self.classes['output']])
# 		values = self.get_class('output')
# 		keys = self.classes['output']
# 		outputs = []
# 		for i in range(len(values)):
# 			output = self.compute(values[i])
# 			outputs.append(output)
# 			self.outputs[keys[i]] = output
# 		return outputs
			
# def conjunction(x):
# 	return False not in x
# def disjunction(x):
# 	return True in x
# def null(x=None):
# 	return None
# def summation(x):
# 	if isinstance(x, list):
# 		return sum(x)


# # print(Execute(summation, [1,2,3]))
# # print(Execute(EXECUTE, [EXECUTE, [EXECUTE, [ANY_TYPE, [[1,True,'3'], bool]]]]))

# function_template = Template().set_all(['function','input','output'])
# model_template = Template().set_all(['input','output'], [Data(['x1','x2','x3']), None])


# f = RelationMemory()
# for i in logical_functions.keys():
# 	f.set(i, logical_functions[i], 'function')

# print(f)
# f.set('x1', 1, 'input')
# f.set('x2', 1, 'input')
# f.set('x3', 1, 'input')
# f.set('y1', 1, 'variable')
# f.set('y2', 1, 'variable')
# f.set('y3', 1, 'variable')
# f.set('sum', summation, 'function')
# f.set('con', conjunction, 'function')
# f.set('dis', disjunction, 'function')

# f.set('f1', function_template.create({
# 		'input':Data(['x1','x2','x3']), 
# 		'function':'con',
# 		'output':'y1'
# 	}), 
# 	'operation'
# )
# f.set('f2', function_template.create({
# 		'input':Data(['x1','x2','x3']), 
# 		'function':'dis',
# 		'output':'y2'
# 	}), 
# 	'operation'
# )
# f.set('f3', function_template.create({
# 	 	'input':Data(['f1', 'f2']),
# 		'function':'NOT_EQUAL',
# 	 	'output':'y3'
# 	}), 
# 	'operation'
# )

# f.set('M1', model_template.create({
# 		'input':'f1', 
# 		'output':'y1'
# 	}), 
# 	'model'
# )
# f.set('M2', model_template.create({
# 		'input':'f2', 
# 		'output':'y2'
# 	}), 
# 	'model'
# )
# f.set('M3', model_template.create({
# 		'input':'f3', 
# 		'output':'y3'
# 	}),
# 	'model', 
# 	'output'
# )

# data = []
# for rounds in range(100):
# 	inputs = [bool(rr(2)) for i in range(3)]
# 	outputs = f(inputs)
# 	data.append(outputs)
# 	print([i for i in outputs])
# for i in data:
# 	print(i)