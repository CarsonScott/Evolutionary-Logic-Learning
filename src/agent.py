from topology import *

class Agent(Topology):
	def __init__(self):
		super().__init__()
		self + ['INPUT', 'OUTPUT', 'HISTORY', 'RUNNING']
		self['RUNNING'] = False
		self['INPUT'] = list()
		self['HISTORY'] = list()

	def __call__(self, pos=None):
		if pos != None:
			self.begin(pos)
			self['OUTPUT'] = out

		self['INPUT'] = self.get_neighborhood(self['OUTPUT'])
		self['OUTPUT'] = self.select()
		y = self['OUTPUT']

		if self['OUTPUT'] == None:
			self.reset()
		else:self['HISTORY'].append(self['OUTPUT'])
		return y
	def create(self, top):
		for i in top.keys():
			self[i] = top[i]
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

	def begin(self, pos):
		self['INPUT'] = []
		self['RUNNING'] = True
		self['HISTORY'] = list()
		self['OUTPUT'] = pos

	def reset(self):
		self['RUNNING'] = False
		self['OUTPUT'] = None
		self['HISTORY'] = list()
		self['INPUT'] = list()

	def select(self):
		pass
