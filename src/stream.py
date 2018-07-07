from lib.util import *

class Stream(list):
	def __init__(self, stores):
		self.size = stores

	def retrieve(self, store):
		return self[store]

	def add(self, data=None):
		prev_store = data
		if len(self) < self.size:
			self.insert(0, data)
			preve_store = self[0]
		for i in range(0, len(self)):
			this_store = self[i]
			self[i] = prev_store
			prev_store = this_store
		return self

