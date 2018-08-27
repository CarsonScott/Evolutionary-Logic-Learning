from functional_logic import *
from matrix import *
from lib.relations import *

class Memory(Schema):
	
	def __init__(self, memory=None):
		self.create(meta_functions)
		self.create(memory)

	def get_all(self, keys):
		values = []
		for i in keys:
			if i in self.keys():
				values.append(self[i])
			else:values.append(i)
		return values

	def set(self, *data):
		for i in range(1, len(data)):
			self[data[i-1]] = data[i]

	def compose(self, key, data):
		X = list(data)
		for i in range(len(X)):
			x = X[i]
			if isinstance(x, str) and x in self.keys():
				X[i] = self[x]
		self.set(key, Compose(*X))

	def compute(self, key, data):
		c = isinstance(data, Collection)
		if isinstance(data, list):
			data = list(data)
		if isinstance(data, list):
			data = self.get_all(data)
			if len(data) == 1:
				data = data[0]
			if c:data = Collection(data)
		elif isinstance(data, str):
			if data in self.keys():
				data = self[data]
		if c:data = Collection(data)
		if isinstance(self[key], list):
			output = []
			for i in range(len(self[key])):
				f = self[key][i]
				if isinstance(f, str) and f in self.keys():
					f = self[f]
				y = Compute(f, data)
				output.append(y)
			return output
		else:
			return Compute(self[key], data)


class MemorySpace(Dictionary):
	def __init__(self, keys=[], vals=[]):
		self.classes = Dictionary()
		self.models = Dictionary()

	def set_classes(self, key, *classes):
		for i in classes:
			if i not in self.classes.keys():
				self.classes[i] = []
			if key not in self.classes[i]:
				self.classes[i].append(key)

	def set_model(self, key, model):
		self.models[key] = model

	def set(self, key, value, *classes):		
		self[key] = value
		self.set_classes(key, *classes)
		self.set_model(key, None)

	def set_values(self, keys, values):
		for i in range(len(keys)):
			val = None
			key = keys[i]
			if i < len(values):
				val = values[i]
			self[key] = val
	
	def generate_model(self, key):
		classes = []
		value = self[key]
		model = MemorySpace()
		classes = self.get_classes(key)
		if classes != None and len(classes) == 0:
			classes = None
		model['key'] = key
		features = MemorySpace()	
		if not key in self.classes.keys():
			for i in range(len(features)):
				val = None
				key = features[i]
				if i < len(values):
					val = values[i]
				features[key] = val
		if classes != None:features['classes'] = classes
		if value != None:features['value'] = value
		if len(features.keys()) > 0:
			self.set_model(key, model)
			model['features'] = features
		
	def generate_models(self):
		for i in self.keys():
			self.generate_model(i)
	
	def get_model(self, key):
		return self.models[key]

	def get_models(self):
		models = []
		for i in self.models.keys():
			model = self.get_model(i)
			if model != None:
				models.append(model)
		return models

	def get_values(self, keys):
		return [self[i] for i in keys]

	def get_classes(self, key):
		classes = []
		if key not in self.classes.keys():
			for i in self.classes.keys():
				if key in self.classes[i]:
					classes.append(i)
			return classes

