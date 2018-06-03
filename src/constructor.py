from lib.util import *

def construct(t, v=None):
	if t in CONSTRUCTORS.keys():
		f = CONSTRUCTORS[t]
		return f(v)

class Constructor(Dict):
	def __init__(self, datatype, default=None):
		self.type = datatype
		self.value = default

	def __call__(self):
		return construct(self.type, self.value)