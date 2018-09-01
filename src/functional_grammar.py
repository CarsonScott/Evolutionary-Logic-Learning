from lib.util import *
from lib.relations import *
from dictionary import *

CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-._'
CHARS = list(CHARS + CHARS.upper())
SPACES = list('	 ')

class Generator(list):
	def __init__(self, open_key='(', close_key=')', accepted=[], ignored=[]):
		self.accepted = union(CHARS, accepted)
		self.ignored = union(SPACES, ignored)
		self.leaf = True
		self.done = False
		self.open = open_key
		self.close = close_key

	def __call__(self, expression):
		self.test(expression)
		output = []
		for c in expression:
			output = self.update(c)
		if len(output) == 1 and isinstance(output[0], Generator):
			output = output[0]
		return list(output)

	def test(self, expression):
		state = 0
		for c in expression:
			if c == self.open:
				state += 1
			elif c == self.close:
				state -= 1
			elif c not in self.accepted and c not in self.ignored:
				raise Exception(c + ' is not a valid character.')
		if state != 0:
			raise Exception(expression + ' is not a valid expression.')

	def update(self, c, root=True):
		if not self.done:
			if self.leaf:
				if c == self.open:
					gen = Generator(self.open, self.close, self.accepted, self.ignored)
					if len(self) > 0 and self[len(self)-1] == '':
						self[len(self)-1] = gen
					else:self.append(gen)
					self.leaf = False
				elif c == self.close:
					self.done = True
				elif c in self.accepted:
					if len(self) == 0 or not isinstance(self[len(self)-1], str):
						self.append(c)
					else:self[len(self)-1] += c
				elif c not in self.ignored:
					self.append(c)
				elif len(self) == 0 or self[len(self)-1] != '':
					self.append('')
			else:
				x = self[len(self)-1]
				if isinstance(x, Generator):
					if c == self.close and x.leaf == True:
						self[len(self)-1].done = True
						self.leaf = True
					self[len(self)-1].update(c, root=False)
		if self.done:
			while '' in self:
				del self[self.index('')]
		return self
		
def transform(model, identifiers):
	if isinstance(model, list):
		output = Dictionary()
		output['type'] = None
		output['body'] = []
		for i in range(len(model)):
			x = model[i]
			x = transform(x, identifiers)
			if not isinstance(x, list):
				x = [x]
			index = None
			head = None
			for j in range(len(x)):
				x[j] = transform(x[j], identifiers)
				if x[j] in identifiers:
					index = j
					head = x[j]
			if head != None:
				output['type'] = head
				x.pop(index)			

			if len(x) == 1:x = x[0]
			if x != []:
				output['body'].append(x)
		if output['type'] != None:
			return output
		else:
			return list(output.values())
	return model

def biased_selection(*data):#options, biases={}):
	space = []
	for i in range(0, len(data), 2):
		option = data[i]
		bias = data[i+1]
		for j in range(bias):
			space.append(option)
	if len(space) > 0:
		return space[rr(len(space))]
	# # while i < len(data):
	# # 	if 
	# # 	i += 1

	# # space = list()
	# # for i in range(len(options)):
	# # 	key = options[i]
	# # 	space.append(key)
	# # for i in biases.keys():
	# # 	for j in range(biases[i]):
	# # 		space.append(i)
	# # selection = space[rr(len(space))]
	# return selection

T = 10000
X = Dictionary()
X + ['a', 'b', 'c']
for i in range(T):
	x = biased_selection('a', 1, 'b', 2, 'c', 3)
	if (x in X.keys() and X[x] == None) or (x not in X.keys()):
		X[x] = 1 / T
	else:
		X[x] += 1 / T

for i in X.keys():
	print(i, X[i])

class Agent(Dictionary):

	def __init__(self):
		self.st_memory = Dictionary()
		self.lt_memory = Dictionary() 

	def convert(self, model):
		if isinstance(model, Dictionary):
			t = model['type']
			b = model['body']
			for i in range(len(b)):
				b[i] = self.convert(b[i])
			if t in self.keys():
				f = self[t]
				return f(model)
		return model

	def update(self, *data):
		outputs = list(data)
		for i in range(len(data)):
			if isinstance(data[i], list) or isinstance(data[i], tuple):
				outputs[i] = self.update(*data[i])
			elif isinstance(data[i], Dictionary):
				outputs[i] = self.compute(data[i])
			elif data[i] in self.keys():
				outputs[i] = self[data[i]]
			else:
				try:
					int_x = int(data[i])
					float_x = float(data[i])
					if int_x == float_x:
						outputs[i] = int_x
					else:outputs[i] = float_x
				except:continue
		if len(outputs) == 1:
			outputs = outputs[0]
		return outputs

	def compute(self, schema):
		t = schema['id']

		if t == 'of':
			f = schema['func']
			x = schema['data']
			f,x = self.update(f,x)
			if isinstance(x, tuple):
				return f(*x)
			else:return f(x)

		elif t == 'is':
			s = schema['data']
			v = schema['refr']
			s,v = self.update(s,v)
			return s == v
		
		elif t == 'if':
			p = schema['body']
			c = schema['cond']
			c = self.update(c)
			p = self.update(p)
		
			if c:return p

		elif t == 'for':
			p = schema['body']
			i = schema['iter']
			v = i['name']
			l = i['list']
			y = []

			has = v in self.keys()
			if has:
				val = self[v]
			for j in range(len(l)):
				x = l[j]
				self[v] = x
				y.append(self.update(p))
			if has:self[v] = val
			else:del self[v]
			return y

def for_schema(model):
	b = model['body']
	m = Dictionary()
	m['id'] = model['type'] 
	m['type'] = 'schema'
	m['body'] = b[0]
	m['iter'] = b[1]
	return m 
def of_schema(model):
	b = model['body']
	f = b[0]
	x = tuple(b[1:])
	if len(x) == 1:
		x = x[0]
	m = Dictionary()
	m['id'] = model['type']
	m['type'] = 'schema'
	m['func'] = f
	m['data'] = x
	return m 
def in_schema(model):
	b = model['body']
	m = Dictionary()
	m['id'] = model['type']
	m['type'] = 'schema'
	m['list'] = b[1]
	m['name'] = b[0]
	return m 
def is_schema(model):
	b = model['body']
	m = Dictionary()
	m['id'] = model['type']
	m['type'] = 'schema'
	m['data'] = b[0]
	m['refr'] = b[1]
	return m
def if_schema(model):
	b = model['body']
	m = Dictionary()
	m['id'] = model['type'] 
	m['type'] = 'schema'
	m['body'] = b[0]
	m['cond'] = b[1]
	return m
def to_schema(model):
	b = model['body']
	i,j = b
	try:i,j = int(i), int(j)
	except:return None
	return [x for x in range(i,j)]

generator = Generator()
generator.accepted += ['.']

agent = Agent()
agent['for'] = for_schema
agent['of'] = of_schema
agent['in'] = in_schema
agent['to'] = to_schema
agent['is'] = is_schema
agent['if'] = if_schema
agent['mul'] = mul
def square(x):
	return x * x
def mul(X):
	y = X[0]
	for i in range(1, len(X)):
		y *= X[i]
	return y

expression = '(((mul of x y) for (x in (0 to 10))) for (y in (0 to 10)))'
model = generator(expression)
model = transform(model, 'for of in to is if'.split())
schema = agent.convert(model)

try:
	output = agent.compute(schema)
	print(output)
	

except error:
	input(error)