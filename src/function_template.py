from dictionary import *

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

def Def(x):
	template = Dictionary()
	template + ['statement', 'model']
	if '=' in x:
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

def Mod(statement):
	model = Template()
	if isinstance(statement, tuple):
		function, input = statement
		model = {'function':function, 'input':input}	
	elif isinstance(statement, list):
		source, target = statement
		source = Mod(source)
		model = {'source':source, 'target':target}
	else:model = statement
	return model

def is_dict(x):
	return isinstance(x, dict)

def Template(statement=None):
	template = Dictionary()
	template['model'] = Dictionary()
	template['statement'] = None
	if statement != None:
		try:return Def(statement)
		except:return None
	return template

class Function(Dictionary):

	def __init__(self, statement='', inputs=[]):
		self['template'] = Template(statement)
		self['inputs'] = inputs

	def __call__(self, X=None):
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
		elif get_type(function) == 'variable' and Template(function) != None:
			return self.execute(Template(function)) 
	
		type = None
		statement = []
		if is_dict(function):
			if 'statement' in function and 'model' in function:
				statement = function['statement']
				function = function['model']
		if is_dict(function):
			if 'source' in function and 'target' in function:type = 0
			elif 'function' in function and 'input' in function:type = 1

		if type == None:
			if is_iterable(function):
				F = list(function)
			else:return function	
		else:F = statement

		if type == 0:
			a,b = F
			self[a] = self.execute(b)
			return self[a]
		elif type == 1:
			f,x = F
			f = self.execute(f)
			if is_iterable(x):
				for i in range(len(x)):
					x[i] = self.execute(x[i])
			else:x = self.execute(x)
			if callable(f):return f(x)
		else:return F

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
	
