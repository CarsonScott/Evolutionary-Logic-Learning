from lib.types import *

class NumericalDomain:
	def __init__(self, lower=INF(-1), upper=INF(1)):
		self.lower = lower
		self.upper = upper
	def __call__(self, value):
		if self.lower != INF(-1):
			if self.lower > value:
				return False
		if self.upper != INF(1):
			if self.upper <= value:
				return False
		return True


class CategoricalDomain:
	def __init__(self, valid=ALL(1), invalid=ALL(-1)):
		self.valid = valid
		self.invalid = invalid
	def __call__(self, value):
		if self.valid != ALL(1):
			if value not in self.valid:
				return False
		if self.invalid != ALL(-1):
			if value in self.invalid:
				return False
		return True

class FunctionConstraint:
	def __call__(self, value):
		return callable(value)

class TypeConstraint:
	def __init__(self, type):
		self.type = type
	def __call__(self, value):
		return identify(value) == self.type