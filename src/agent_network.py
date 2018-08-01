from agent import *

class unknown:
	pass

class Model(Dictionary):

	def __init__(self, properties):
		super().__init__()
		for i in properties:
			self[i] = unknown

	def label(self, property):
		if self[property] == unknown:
			return 'free'
		return 'known'

	def template(self):
		y = Dictionary({'known':[], 'free':[]})
		for i in self.keys():
			c = self.label(i)
			if i not in y[c]: 
				y[c].append(i)
		return y['known'], y['free']
		
	def __mul__(self, model):
		y = Model(union(self.keys(), model.keys()))
		keys = intersection(self, model)
		for i in keys:
			if self.label(i) == 'known':
				y[i] = self[i]
			elif model.label(i) == 'known':
				y[i] = model[i]
		keys = compliment(model, self)
		for i in keys:
			if self.label(i) == 'known':
				y[i] = self[i]
		keys = compliment(self, model)
		for i in keys:
			if model.label(i) == 'known':
				y[i] = model[i]
		return y

m1 = Model(['a', 'b', 'c'])
m2 = Model(['a', 'b', 'c'])
m3 = Model(['c', 'd', 'e'])
m1['a'] = 5
m1['b'] = 0.5
m2['d'] = 0.1
m2['c'] = 10
m3['e'] = 100

print(m1 * m2 * m3)

class RelationNetwork(Dictionary):
	def __init__(self, sensors, motors, size):
		self.step = None
		self.paths = None
		self.points = None
		self.sensors = []
		self.motors = []
		self.memory = [list(), list()]
		self.capacity = size
		self.topology = Topology()
		self.previous = Topology()
		self.appeared = None
		self.disappeared = None
		for i in range(sensors):
			self.sensors.append([])
		for i in range(motors):
			self.motors.append([])
	def set_sensor(self, key, value):
		self.sensors[key] = value
	def get_motor(self, key):
		return self.motors[key]
	def clear_sensors(self):
		for i in range(len(self.sensors)):
			self.sensors[i] = []
	def clear_motors(self):
		for i in range(len(self.motors)):
			self.motors[i] = []

	def update(self):
		if self.step == None:
			self.step = 0
		else:self.step += 1

		self.clear_motors()
		update_memory = False
		for i in range(len(self.sensors)):
			data = self.sensors[i]
			if data != None:
				for x in data:
					if x not in self.memory:
						src = str(x)
						rel = ' type '
						dst = str(i)
						statement = src,rel,dst
						self.memory[1].append(statement)
						self.memory[0].append(src)
						update_memory = True

		if not update_memory:
			self.memory.append(None)
		if len(self.memory[0]) > self.capacity:
			for i in range(len(self.memory)):
				mem = self.memory[i]
				mem = mem[len(mem)-self.capacity:len(mem)]
				self.memory[i] = mem
		self.clear_sensors()

	def process(self):
		points = []
		paths = []
		points, paths = self.memory
		points = reverse(points)
		paths = reverse(paths)
		
		self.previous = self.topology
		self.paths = paths
		self.points = points
		self.topology = topology
		for i in range(len(self.paths)):
			self.paths[i] = merge('', self.paths[i])
		
	def compare(self):
		Ti = self.previous
		Tf = self.topology
		self.topology.set_point(random_str(5), intersection(Ti, Tf))
		A = compliment(Ti, Tf) 
		D = compliment(Tf, Ti) 
		self.appeared = A
		self.disappeared = D

	def compute(self):
		return Dictionary({
			'new objects': self.points,
			'new relations': self.paths,
			'recently stored': self.appeared,
			'recently removed': self.disappeared,
			'current time': self.step,
		})

from graphics import *

net = RelationNetwork(10, 10, 10)
opt = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(' ')
top = []
net['points'] = opt
lines = Dictionary()
shapes = Dictionary()
for i in range(10000):
	s = rr(len(net.sensors))
	x = opt[rr(len(opt))]
	net.sensors[s].append(x)

	net.update()
	net.process()
	net.compare()
	y=net.compute()

	top += net.topology
	S,L = visualize(top)
	main(S, L)

