from function_language import *

def Null(*x):
	return None

class Composition:
	def __init__(self, *functions):
		self.functions = functions
	def __call__(self, input):
		F = self.functions
		x = input
		y = None
		for f in F:
			y = f(x)
			x = y
		return y

class Topology(Automaton):
	
	def __init__(self, pnt=Dictionary(), pat=Dictionary()):
		if 'paths' not in self.keys(): 
			self['paths'] = Dictionary()
		self.assign_points(pnt)
		self.assign_paths(pat)
	def assign_points(self, points):
		if isinstance(points, dict):
			for i in points.keys():
				self.set_point(str(i))
		elif isinstance(points, list):
			for i in range(len(points)):
				self.set_point('x' + str(i))

	def assign_paths(self, paths):
		if isinstance(paths, dict):
			for i in paths.keys():
				p = paths[i]
				src = None
				dst = None
				rel = None
				if len(p) == 3:src, rel, dst = p
				elif len(p) == 2:src, dst = p
				self.set_path(src, dst, rel)

		elif isinstance(paths, list):
			for i in range(len(paths)):
				p = paths[i]
				src = None
				dst = None
				rel = None
				if len(p) == 3:src, rel, dst = p
				elif len(p) == 2:src, dst = p
				self.set_path(src, dst, 'r' + rel)
				p = paths[i]

	def get_keys(self):
		return self.keys() + self['paths'].keys()
	
	def get_point(self, key):
		return self[key]

	def get_path(self, key):
		return self['paths'][key]
	
	def has_point(self, key):
		return key in self.keys()

	def has_path(self, key):
		return key in self['paths'].keys()
	
	def set_point(self, key, val=None):
		self[key] = val		

	def set_path(self, src, dst, val=None):
		key = src, dst
		if not self.has_path(key):
			path = list()
			if val != None:path.append(val)
			self['paths'][key] = path
		elif val not in self.get_path(key):
			self['paths'][key].append(val)
	
	def get_neighborhood(self, key, ord=True):
		nbr = []
		for i in self['paths'].keys():
			src, dst = i
			if src == key:
				nbr.append(dst)
			elif not ord:
				if dst == key:
					nbr.append(src)
		return nbr

	def get_diagram(self):
		diagram = Dictionary()
		for i in self.keys():
			neighborhood = self.get_neighborhood(i)
			diagram[i] = neighborhood
		return diagram

	def store(self, key, val):
		if not self.has_path(key):
			path = list()
			if val != None:
				path.append(val)
			self['paths'][key] = path
		elif val not in self.get_path(key):
			self['paths'][key].append(val)

	def generate(self, src, dst):
		key = src, dst
		if not self.has_path(key):
			Nsrc = self.get_neighborhood(src)
			for i in range(len(Nsrc)):
				Ndst = self.get_neighborhood(Nsrc[i])
				if dst in Ndst:
					k1 = src, Nsrc[i]
					k2 = Nsrc[i], dst
					p1 = self.get_path(k1)
					p2 = self.get_path(k2)
					p = Composition(p1, p2)
					k = src, dst
					self.store(k, p)
					return True
		return False

def random_topology(points, paths):
	top = Topology()
	for i in range(points):
		top.set_point(str(i))
	keys = top.get_keys()
	for i in range(paths):
		j = rr(len(keys))
		k = rr(len(keys))
		if j != k:
			top.set_path(keys[j], keys[k])
	return top

def convert_topology(points, paths):
	top = Topology()
	
	for i in data.keys():
		x = data[i]
		print(x, data, i)
		if isinstance(x, tuple):# and len(x) == 3:
			# src,rel,dst = x
			if 'paths' not in top.keys():
				top['paths'] = Dictionary()
			top['paths'].append(x)
		elif identify(x) == 'str':
			top[x] = None
		else:
			print('COULD NOT CONVERT: ', x)
	return top