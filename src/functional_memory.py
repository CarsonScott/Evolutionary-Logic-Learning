from dictionary import *

class FunctionMemory(Dictionary):
	def keys(self):
		keys = []
		for i in super().keys():
			if isinstance(i,str) and '.' not in i:
				keys.append(i)
		return keys
	def has(self, key):
		return key in super().keys()
	def get_values(self, keys):
		values = []
		for i in keys:
			value = super().__getitem__(i)
			values.append(value)
		return values
	def set_values(self, keys, values):
		values = []
		index = 0

		for i in keys:
			self[i] = values[index]
			index += 1
			print(self[i], index)
		# 	# value = super().__getitem__(i)
		# 	# values.append(value)
		# return values
	def get_dependent(self, key, ext=None):
		if ext == None:
			ext = key
			key = ''
		i = merge('.', [str(key), str(ext)])
		return self[i]
	def set_dependent(self, key, ext=None, val=None):
		if val == None:
			val = ext
			ext = key
			key = ''
		i = merge('.', [str(key), str(ext)])
		self[i] = val
	def dependencies(self, key):
		out = []
		for i in super().keys():
			if '.' in i:
				index = i.index('.')
				if i[:index] == key:
					out.append(i[index+1:])
		return out