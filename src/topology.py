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

class Topology:
	
	def __init__(self, pnt=Dictionary(), pat=Dictionary()):
		self.points = pnt
		self.paths = pat

	def get_keys(self):
		return self.points.keys() + self.paths.keys()
	
	def get_point(self, key):
		return self.points[key]

	def get_path(self, key):
		return self.paths[key]
	
	def has_point(self, key):
		return key in self.points.keys()

	def has_path(self, key):
		return key in self.paths.keys()
	
	def set_point(self, key, val=None):
		self.points[key] = val		

	def set_path(self, src, dst, val=None):
		key = src, dst
		if not self.has_path(key):
			path = list()
			if val != None:
				path.append(val)
			self.paths[key] = path
		elif val not in self.get_path(key):
			self.paths[key].append(val)
	
	def get_neighborhood(self, key, ord=True):
		nbr = []
		for i in self.paths.keys():
			src, dst = i
			if src == key:
				nbr.append(dst)
			elif not ord:
				if dst == key:
					nbr.append(src)
		return nbr

	def store(self, key, val):
		if not self.has_path(key):
			path = list()
			if val != None:
				path.append(val)
			self.paths[key] = path
		elif val not in self.get_path(key):
			self.paths[key].append(val)

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

class Agent(Topology):
	def __init__(self):
		super().__init__()
		self.output = None
		self.inout = None
		self.running = False
		self.history = None
	def __call__(self, pos=None):
		if pos != None:
			self.begin(pos)
			self.output = out
		y = None
		x = self.get_neighborhood(self.output)
		y = self.select(x)

		if y == None:
			self.reset()
		else:
			self.history.append(y)
			self.input = x
			self.output = y
	def create(self, top):
		super().__init__(top.points, top.paths)
	def compare(self, keys):
		k = keys[0]
		for i in keys[1:]:
			if not self.has_path((k, i)):
				return False
			k = i
		return True
	def search(self, src, dst):
		if self.has_path((src, dst)):
			return [src, dst]
		else:
			N = self.get_neighborhood(src)
			for s in N:
				out = self.search(s, dst)
				if out != []:
					return [src] + out
	def select(self, opt):
		if len(opt) > 0:
			return opt[rr(len(opt))]
	def begin(self, pos):
		self.running = True
		self.history = list()
		self.output = pos
	def reset(self):
		self.running = False
		self.output = None
		self.input = None
def random_topology(points, paths):
	top = Topology()
	for i in range(points):
		top.set_point(str(i))
	keys = top.get_keys()
	for i in range(paths):
		j = rr(len(keys))
		k = rr(len(keys))
		top.set_path(keys[j], keys[k])
	return top

class DFSearcher(Agent):
	def select(self, opt):
		for k in opt:
			if k not in self.history:
				return k

# Detects loops in topological space
class LoopDetector(Agent):
	def select(self, opt):
		if len(self.history) == 0 or self.history[len(self.history)-1] not in self.history[0:len(self.history)-1]:
			for k in opt:
				if k in self.history:
					return k
			if len(opt) > 0:
				return opt[rr(len(opt))]

if __name__ == "__main__":
	# top = Topology()
	# top.set_point('a')
	# top.set_point('b')
	# top.set_point('c')
	# top.set_point('d')
	# top.set_point('e')

	# top.set_path('a', 'b', Null)
	# top.set_path('a', 'c', Null)
	# top.set_path('c', 'b', Null)
	# top.set_path('b', 'd', Null)
	# top.set_path('b', 'e', Null)
	# top.set_path('e', 'b', Null)
	# top.generate('a', 'd')
	top = random_topology(50, 100)

	a = Agent()
	a.create(top)
	options = []
	for i in a.points.keys():
		if a.get_neighborhood(i) != []:
			options.append(i)

	target = options[rr(len(options))]
	a.begin(options[rr(len(options))])

	path = []
	trials = 1000
	for i in range(trials):
		x = options[rr(len(options))]
		y = a.generate(x, target)
		if y:
			print('\n' + str(x) + ' ~> ' + str(target))
			break
	print('performance: ' + str(1 - (i+1)/trials) + '\n')

