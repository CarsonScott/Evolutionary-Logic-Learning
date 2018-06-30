from lib.util import *
from lib.relations import *

class Relation(Dict):
	def __init__(self, type, data):
		self['type'] = type
		self['data'] = data

class Object(Dict):
	def __init__(self):
		self['_dependent'] = Dict()
		self.conjunct = 'conjunction'
		self.sequence = 'consequence'

		self.relations = {'conjunction':{'inputs':['initial', 'final'],
										 'dtypes':['variable', 'variable']},

						  'consequence':{'inputs':['initial', 'final'],
										 'dtypes':['variable', 'variable']}}

		self.operators = {'create':{'inputs':['key', 'type', 'group'],
									'dtypes':['data', 'relation', 'data']},
   						
						  'combine':{'inputs':['initial', 'final'],
									 'dtypes':['variable', 'variable']},
						
						  'depends':{'inputs':['initial', 'final'],
									 'dtypes':['variable', 'variable']}}

	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		self.set_dependence(key)

	def compare(self, initial, final):
		a = self[initial]
		b = self[final]
		sign = '!='
		if isinstance(a, Relation) and isinstance(b, Relation):
			if a['type'] == b['type']:
				t  = a['type']
				Xa = a['data']
				Xb = b['data']
				if t == self.conjunct and equivalent(Xa, Xb):
						return True
				elif t == self.sequence and Xa == Xb:
						return True
		elif self[a] == self[b]:
			return True
		return False

	def types(self):
		return self.relations.keys()

	def keys(self):
		return self['_dependent'].keys()

	def ops(self):
		return self.operators.keys()

	def dependent(self, i):
		if i not in self.keys():
			self['_dependent'][i] = Dict()
		return self['_dependent'][i]

	def set_dependence(self, initial, final=None, label=None):
		if initial not in self.keys():
			self['_dependent'][initial] = Dict()
		if final != None:
			self['_dependent'][initial][final] = label

	def combine(self, a, b):
		order = [a, b]
		if self.compare(a, b):
			Da = self.dependent(a)
			Db = self.dependent(b)
			if len(Da) > len(Db): order = [b, a]
			new, old = order
			for i in self.keys():
				dependent = self.dependent(i)
				if old in dependent.keys():
					dependency = dependent[old]
					del dependent[old]
					dependent[new] = dependency
				self['_dependent'][i] = dependent
			del self['_dependent'][old]
			del self[old]
			return new
		return None

	def create(self, key, type, data):
		self[key] = Relation(type, data)
		self.set_dependence(key)
		for index in data:
			self.set_dependence(index, key, type)

