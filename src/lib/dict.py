from lib.util import *
from lib.data import *

class Dictionary(Dict):
	def __contains__(self, key):
		return key in self.keys()

	def __add__(self, key):
		if identify(key) == 'tuple':
			key, value = key
			self[key] = value
		elif identify(key) == 'list':
			for i in key:
				self + i
		else:self[key] = None

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
