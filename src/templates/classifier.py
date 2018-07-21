from templates.function import *

class Classifier(Function):
	def assign(self, key, *labels):
		for label in labels:
			if key not in self:
				self + (key, List())
			if label not in self:
				self + (label, List())
			if key not in self[label]:
				self[label].append(key)
			if label not in self[key]:
				self[key].append(label)
	def __init__(self, classes):
		for c in classes:
			self + (c, List())
