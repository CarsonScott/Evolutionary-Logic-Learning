from template import *

class Pointer(Template):
	def __init__(self, index=None):
		super().__init__()
		self.assign(0, 'index')
		self.store('index', index)

class Relation(Template):
	def __init__(self, inputs, function=None):
		super().__init__()
		X = []
		for i in range(inputs):
			self.assign(i, 'input')
			X.append(False)
		self.store('input', X)
		index = len(self.keys())
		self.assign(index, 'function')
		self.store('function', function)

class Transmitter(Template):
	def __init__(self, terminal=None, target=None):
		super().__init__()
		self.assign(0, 'terminal')
		self.assign(1, 'target')
		self.store('terminal', terminal)
		self.store('target', target)

class Manipulator(Template):
	def __init__(self, function=None):
		super().__init__()
		self.assign(0, 'action')
		self.assign(1, 'system')
		self.store('action', function)
		self.store('system', Dict())

class Rule(Template):
	def __init__(self, condition=None, response=None):
		super().__init__(True)
		self.assign(0, 'condition')
		self.assign(1, 'response')
		self.store('condition', condition)
		self.store('response', response)
		self.restrict('response', TypeConstraint('manipulator'))