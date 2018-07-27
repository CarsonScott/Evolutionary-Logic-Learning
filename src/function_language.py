from dictionary import *
from lib.relations import *

def get_type(object):
	if identify(object) == 'tuple':
		output = 'function'
	elif identify(object) == 'list':
		output = 'collection'
	elif identify(object) == 'str':
		output = 'variable'
	else:output = 'value'
	return output

def is_iterable(object):
	type = get_type(object)
	if type in ['function', 'collection']:
		output = True
	else: output = False
	return output

def is_nested(object):
	if is_iterable(object):
		for i in range(len(object)):
			if is_iterable(object[i]):
				return True
	return False

def is_valid(object):
	if is_iterable(object):
		if is_nested(object):
			output = True
			for i in range(len(object)):
				if not is_valid(object[i]):
					return False
	return True

def plugin(data, function):
	type = get_type(function)
	output = function
	if is_iterable(function):
		output = []
		for i in range(len(function)):
			f = function[i]
			if is_iterable(f):
				y = plugin(data, f)
			elif f in data:
				y = data[f]
			else:y = function[i]
			output.append(y)
	elif function in data:
		output = data[function]
	if type == 'function':
		return tuple(output)
	elif type == 'collection':
		return list(output)
	return output

def identify_model(x):
	if not isinstance(x, Dictionary):
		return None
	types = Dictionary({'store-statement':('source', 'target'),
		 				 'else-statement':('statement', 'output'),
		 				 'call-statement':('function', 'input'),
		 				   'if-statement':('condition', 'output')})
	for key in types.keys():
		v = types[key]
		if equivalent(x.keys(), v):
			return key

def Def(x):
	x = remove(x, ' ')
	template = Dictionary()
	template + ['statement', 'model']

	if '/' in x:
		i = x.index('/')
		c = x[:i]
		s = x[i+1:]
		mc = Def(c)
		ms = Def(s)
		statement = [c, s]
		model = Dictionary({'statement':c, 'output':s})
		statement[0] = mc['statement']
		model['statement'] = mc['model']
		if mc == c: 
			return None
		if ms != s:
			statement[1] = ms['statement']
			model['output'] = ms['model']
		template['statement'] = statement
		template['model'] = model

	elif ':' in x:
		i = x.index(':')
		c = x[:i]
		s = x[i+1:]
		mc = Def(c)
		ms = Def(s)
		statement = [c, s]
		model = Dictionary({'condition':c, 'output':s})
		if c == '': 
			return Def(s)
		if mc != c:
			statement[0] = mc['statement']
			model['condition'] = mc['model']
		if ms != s:
			statement[1] = ms['statement']
			model['output'] = ms['model']
		template['statement'] = statement
		template['model'] = model

	elif '=' in x:
		i = x.index('=')
		s = x[:i]
		t = x[i+1:]
		m = Def(s)
		if s != m:
			template['statement'] = [m['statement'], t]
			template['model'] = Dictionary({'source':m['model'], 'target':t})
		else:
			template['statement'] = [s, t]
			template['model'] = Dictionary({'source':s, 'target':t})

	elif '(' in x and ')' in x:
		i = x.index('(')
		j = len(x) - x[::-1].index(')') - 1
		f = x[:i]
		x = x[i+1:j]
		x = Def(x)
		template['statement'] = (f, x)
		template['model'] = Dictionary({'function':f, 'input':x})
	elif ',' in x:
		return x.split(',')
	else:return x
	return template

def is_dict(x):
	return isinstance(x, dict)

def create_template(statement=None):
	template = Dictionary()
	template['model'] = Dictionary()
	template['statement'] = None
	if statement != None:
		return Def(statement)
	return template

class Function(Dictionary):

	def __init__(self, statement='', inputs=[]):
		self['template'] = create_template(statement)
		self['inputs'] = inputs

	def __call__(self, *X):
		X = list(X)
		if isinstance(X, list):
			for i in range(len(X)):
				key = self['inputs'][i]
				self[key] = X[i]
		elif isinstance(X, dict):
			keys = X.keys()
			for i in keys:
				self[i] = X[i]
		template = self['template']
		return self.execute(template)

	def execute(self, function):
		if function in self:
			return self.execute(self[function])
		elif isinstance(function, Function):
			return self.execute(function['template'])
		elif get_type(function) == 'variable' and create_template(function) != None:
			return self.execute(create_template(function)) 
	
		model = None
		if is_dict(function):
			if equivalent(['statement', 'model'], function.keys()):
				model = function['model']
			else:model = function

		type = identify_model(model)
		if type == None and identify_model(function) != None:
			type = identify_model(function)
			model = function
		elif type == None:return function
		
		if type == 'else-statement':
			s,y = model['statement'], model['output']
			if is_dict(s):
				c = s['condition']
				if not self.execute(c):
					return self.execute(y)
				else:return self.execute(s)

		elif type == 'if-statement':
			c,y = model['condition'], model['output']
			c = self.execute(c)
			if c:return self.execute(y)

		elif type == 'store-statement':
			a,b = model['source'], model['target']
			self[a] = self.execute(b)
			return self[a]

		elif type == 'call-statement':
			f,x = model['function'], model['input']
			f = self.execute(f)
			if is_iterable(x):
				for i in range(len(x)):
					x[i] = self.execute(x[i])
			else:x = self.execute(x)
			if callable(f):return f(x)
		
		else:return function['model']

class Operator(Dictionary):
	
	def __init__(self, function, types):
		self['function'] = function
		self['input'] = Dictionary()
		for i in range(len(types)):
			t = types[i]
			self['input'][i] = t
	
	def __call__(self, x):
		size = self.size()
		function = self['function']
		if size != 1:
			if iterable(x):
				if len(x) == size:
					for i in range(size):
						if self['input'][i] != identify(x[i]):
							return
					return function(*x)
		else:
			if self['input'][0] == identify(x):
				return function(x)
			elif self['input'][0] == identify(x[0]):
				return function(x[0])
		return
	
	def size(self):
		return len(self['input'])
	