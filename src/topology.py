from function_template import *




# class Topology(Dictionary):
# 	def __init__(self, nodes=[]):
# 		super().__init__()
# 		self.obj(nodes)

# 	def obj(self, key):
# 		if iterable(key):
# 			for k in key:
# 				self.obj(k)
# 		elif key not in self:
# 			self[key] = Dictionary() 

# 	def rel(self, keys):
# 		k1 = keys[0]
# 		if not self.has_node(k1):
# 			self.obj(k1)
# 		for k2 in keys[1:]:
# 			if not self.has_link(k1, k2):
# 				self[k1][k2] = None

# 	def has_node(self, key):
# 		return key in self

# 	def has_link(self, key1, key2):
# 		return self.has_node(key1) and key2 in self[key1]

# top = Topology(['a', 'b', 'c'])
# top.obj(['a', 'b', 'c', 'd'])
# top.rel(['a', 'b'])

