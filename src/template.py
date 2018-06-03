from lib.functions import *
from lib.constraints import *
from lib.util import *

class Template(Dict):
	def __init__(self):
		self.labels = Dict()

	def add_constraint(self, label, key, constraint):
		C = self[-1]
		if label not in C.keys():
			C[label] = Dict()

		if key not in C[label].keys():
			C[label][key] = []

		C[label][key].append(constraint)
		self[-1] = C 
	
	def store(self, label, values):
		indices = self.retrieve(label)
		if isinstance(values, list):
			for i in range(len(indices)):
				index = indices[i]
				self[index] = values[i]
		elif len(indices) > 0:
			index = indices[0]
			self[index] = values

	def append(self, value):
		index = len(self)
		self.assign(index, value)
	
	def assign(self, index, label):
		if index not in self.keys():
			self[index] = None
		if label not in self.labels.keys():
			self.labels[label] = []
		self.labels[label].append(index)
	
	def retrieve(self, label):
		if label in self.labels.keys():
			return self.labels[label]
		else:raise Exception(str(label) + ' not found') 
	
	def translate(self, indices):
		output = []
		if len(indices) == 1:
			index = indices[0]
			output = self[index]
		else:
			for i in indices:
				output.append(self[i])
		return output
	
	def compile(self):
		labels = Dict()
		# labels = [None for i in range(len(self))]
		for i in self.labels.keys():
			for j in self.labels[i]:
				labels[j] = i
		return labels
	
	def generate(self):
		instance = Template()
		for i in self.labels.keys():
			instance[i] = Dict()
			for j in range(len(self.labels[i])):
				index = self.labels[i][j]
				instance[i][j] = self[index]
		return instance
	
	def compute(self, values):
		indices = self.retrieve('variable')
		c = 0
		for i in indices:
			self[i] = values[c]
			c += 1
		self.generate()
	
	def validity(self, label):
		ratings = Dict()
		for i in self.retrieve(label):
			ratings[i] = 0
			if label in self[-1].keys():
				for constraint in self[-1][label]:
					ratings[i] += 1/len(self[-1][label])
			else:ratings[i] = 1
		output = sum(list(ratings.values()))
		if len(ratings) > 0:
			output /= len(ratings)
		return output

	def restrict(self, label, constraint):
		C = self[-1]
		if label not in C.keys():
			C[label] = []
		C[label].append(constraint)
		self[-1] = C
	
	def utility(self):
		rating = 0
		for i in self.labels.keys():
			rating += self.rate(i)
		if len(self.labels.keys()) > 0:
			rating /= len(self.labels.keys())
		else:rating = 1
		return rating
	
	def info(self, type):
		info = Dict()
		info['type'] = type
		info['variables'] = Dict()
		info['constraints'] = Dict()
		for i in self.retrieve(type):
			info['variables'][i] = self[i]
		if type in self[-1].keys():
			info['constraints'] = self[-1][type]
		return info

	def get(self, label):
		if label in self.labels.keys():
			return self.translate(self.retrieve(label))
