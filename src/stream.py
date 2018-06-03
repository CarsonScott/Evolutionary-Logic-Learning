from lib.util import *

class Stream:
	def __init__(self, stores):
		self.stores = [[] for i in range(stores)]

	def retrieve(self, store):
		return self.stores[store]

	def update(self, data=None):
		prev_store = data
		for i in range(0, len(self.stores)):
			this_store = self.stores[i]
			self.stores[i] = prev_store
			prev_store = this_store
		return self.stores
