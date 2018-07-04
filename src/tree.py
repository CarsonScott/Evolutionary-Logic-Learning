from lib.util import *
from copy import deepcopy

class NestedList(list):
	def __init__(self, data=None):
		if data != None:
			if isinstance(data, int):
				for i in range(data):
					self.append(None)
			elif isinstance(data, list):
				for i in range(len(data)):
					self.append(data[i])
		self.capacity = len(self)
	def __setitem__(self, index, value):
		if index < len(self):
			if isinstance(self[index], Tree):
				self[index][0] = value
			else:super().__setitem__(index, value)
		else:self.append(value)
			
	def at_capacity(self):
		return len(self) > self.capacity

	def create(self, *data):
		values = list(data)
		error = len(values) - len(self)
		for i in range(len(values)):
			value = values[i]
			if isinstance(value, Tree):
				constructor = self.__class__
				value = constructor(value) 
			if i >= len(self):
				self.append(value)
			else:self[i] = value
		self.capacity = len(self)
		return self
	def reset(self, data=None):
		del self[0:len(self)]
		if data != None:
			self.create(*data)

class Tree(NestedList):
	def get_root(self):
		return self[0]
	def set_root(self, value):
		self[0] = value
	def get_children(self):
		return self[1:]
	def set_children(self, values):
		for i in range(len(values)):
			self[i+1] = values[i]
	def display(self, indent='', top=True):
		root = self.get_root()
		children = self.get_children()
		string = indent + str(root) + '\n'
		new_indent = '|-' + indent
		for i in range(len(children)):
			if isinstance(children[i], Tree):
				s = children[i].display(new_indent, False)
			else:s = new_indent + str(children[i]) + ';\n'
			string += s
		if not top:return string
		else:print(string)
	def rotate(self, index):
		tree = deepcopy(self)
		ratio = (index-1) / (len(tree)-1)
		if ratio < 0.5:
			direction = 'left'
		else:direction = 'right'
		new_tree = tree[index]
		del tree[index]
		if direction == 'left':
			new_tree.append(tree)
			if new_tree.is_valid() == False:
				data = new_tree[2]
				del new_tree[2]
				new_tree[len(new_tree)-1].insert(1, data)
		elif direction == 'right':
			new_tree.insert(1, tree)
			if new_tree.at_capacity():
				data = new_tree[len(new_tree)-2]
				del new_tree[len(new_tree)-2]
				new_tree[1].append(data)
		self.reset(new_tree)

# t = Tree(2)
# t[0] = 'a'
# t[1] = 'c'
# t[2] = Tree(['b', 'd', 'e'])

# t.display()
# t.rotate(2)
# t.display()

