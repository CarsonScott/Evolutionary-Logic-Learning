from lib.util import *
from matrix import *

class List(list):
	def __str__(self, tab='', inc='  '):
		rooted = False
		for key in range(len(self)):
			if isinstance(self[key], list):
				rooted = True
				break

		string = ''
		strings = []
		if rooted:
			for key in range(len(self)):
				strings.append(tab + str(key) + '[')
				strings.append(tab + str(key) + '[' + self[key].__str__(tab + inc, inc) + ']')
			else:
				strings.append(tab + '[' + str(key) + str(self[key]) + ']')
		else:
			strings.append(tab + '[' + merge(', ', self))

		strings = merge('\n', strings)
		return strings + ']'


	def __add__(self, value):
		if iterable(value):
			return super().__add__(value)
		else: self + [value]
	def __sub__(self, value):
		if iterable(value):
			for v in value:
				self - v
		elif v in self:
			del self[self.index(v)]


class Dictionary(Dict):
	def __contains__(self, key):
		return key in self.keys()

	def __add__(self, key):
		value = None
		if identify(key) == 'tuple':
			key, value = key

			self[key] = value
		elif identify(key) == 'list':
			# value = None
			for i in key:
				self + i
				if identify(value) == 'list':
					self + (i, value[i])
				else:
					self + (i, value)
		else:self[key] = value
		return self
	def __sub__(self, key):
		if identify(key) == 'list':
			for i in key:
				self - i
		else:del self[key]

	def compile(self, keys):
		output = Dictionary()
		for i in keys:
			if i in self:
				output[i] = self[i]
		return output

	def translate(self, key):
		if identify(key) == 'list':
			return [self.translate(i) for i in key]
		elif key in self:
			return self[key]
		return key
