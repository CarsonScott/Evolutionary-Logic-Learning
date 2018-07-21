from dictionary import *

class Function(Dictionary):
	def __call__(self, key):
		return self.translate(key)