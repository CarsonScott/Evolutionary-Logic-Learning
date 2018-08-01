from agent import *
import time
from matrix import *
from operator import add
from function_language import *
from graphics import *
from math import tanh,sin,cos,pi,sqrt,atan2

# Inc = Function('x=tanh(y)', ['x'])
# Inc['add'] = ADD
# Inc['tanh'] = tanh
# Inc['y'] = 'add(x,dx)'
# Inc['x'] = 0.0
# Inc['dx'] = 0.4

# Dec = Function('x=tanh(y)', ['x'])
# Dec['y'] = 'add(x,dx)'
# Dec['add'] = ADD
# Dec['tanh'] = tanh
# Dec['x'] = 0.0
# Dec['dx'] = -0.4

# Sin = Function('sin(input)', ['input'])
# Sin['sin'] = sin
# Sin['input'] = 0

# controller = Automaton(['L:X=inc(X)','R:X=dec(X)', 'Y=sin(X)'], inputs=['L', 'R'], outputs=['Y'])
# controller['X'] = 0.0
# controller['Y'] = 0.0
# controller['L'] = False
# controller['R'] = False
# controller['inc'] = Inc
# controller['dec'] = Dec
# controller['sin'] = sin

# for i in range(100):
# 	L,R = bool(rr(2)),bool(rr(2))
# 	print(controller(L,R))
# 	print(controller['Y'])

class EuclideanSpace(Dictionary):
	def get_distance(self, src, dst):
		p1 = self[src]
		p2 = self[dst]
		x1,y1 = p1
		x2,y2 = p2
		return sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))
	def get_angle(self, src, dst):
		p1 = self[src]
		p2 = self[dst]
		x1,y1 = p1
		x2,y2 = p2
		return atan2(y2-y1, x2-x1)
	def get_topology(self, threshold):
		top = Topology()
		for i in range(len(self.keys())):
			ki = self.keys()[i]
			top.set_point(ki)
			for j in range(i, len(self.keys())):
				if i == j:continue
				kj = self.keys()[j]
				top.set_point(kj)
				dij = self.get_distance(ki, kj)
				if dij <= threshold:
					aij = self.get_angle(ki, kj)
					Rij = Matrix([dij, aij])
					top.set_path(ki, kj, dij)
					top.set_path(ki, kj, aij)
		return top

def random_euclidean(dimensions, points):
	width, height = dimensions
	space = EuclideanSpace()
	for i in range(points):
		x = rr(width)
		y = rr(height)
		position = Matrix([x, y])
		space[i] = position
	return space

# space = random_euclidean(Matrix([100, 100]), 75)
# topology = space.get_topology(25)
# p1,p2 = visualize(topology)
# for i in range(1000):
# # 	main(p1,p2)


# for i in topology.keys():
# 	print(i, topology.get_neighborhood(i))
# print(topology.get_diagram())

def compute_weight(x,):
	a = sin(x)
	y = tanh(-abs(a-pi/2)/(pi))
	return y

class RandomWalker(Agent):
	def select(self):
		x = self['INPUT']
		if len(x) > 0:
			return x[rr(len(x))]

# Performs depth-first search in topological space
class DepthFirstSearch(Agent):
	def select(self):
		x = self['INPUT']
		for k in x:
			if k not in self['HISTORY']:
				return k

# Detects loops in topological space
class LoopDetector(Agent):
	def select(self):
		x = self['INPUT']
		if len(self['HISTORY']) == 0 or self['HISTORY'][len(self['HISTORY'])-1] not in self['HISTORY'][0:len(self['HISTORY'])-1]:
			for k in x:
				if k in self['HISTORY']:return k
			if len(x) > 0:return x[rr(len(x))]


# class FunctionalAgent(Agent):
# 	def select(self, x):


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
	top = random_topology(50, 50)
	a = Agent()
	a.create(top)
	# a.create(top)
	xions = []
	for i in a.get_keys():
		if a.get_neighborhood(i) != []:
			xions.append(i)

	target = xions[rr(len(xions))]
	a.begin(xions[rr(len(xions))])

	p1 = []
	p2 = []
	path = []
	trials = 1000
	print(len(a['paths'].keys()), '\n')
	for i in range(trials):
		history = a['HISTORY']
		print(a())
		if not a['RUNNING']:
			path.append(history)
			print()
			a = Agent()
			a.create(top)
		P,L = visualize(a)
		p1 = union(p1, P)
		p2 = union(p2, L)
		main(p1,p2)
		time.sleep(0.1)
	print(path)
	# print('performance: ' + str(1 - (i+1)/trials) + '\n')
# def ID(x):
# 	return x
# def AND(x):
# 	for i in x:
# 		if not i:return False
# 	return True
# def OR(x):
# 	for i in x:
# 		if i: return True
# 	return False

# am = Automaton(['c = div(f,g)', 'b = add(d,e)', 'a = mul(b,c)'], ['d', 'e', 'f', 'g'], ['a', 'b', 'c', 'd'])
# am + 'a b c d e f mul add div'.split(' ')
# am['a'] = 0
# am['b'] = 0
# am['c'] = 0
# am['d'] = 0
# am['e'] = 0
# am['f'] = 0
# am['g'] = 0
# am['add'] = ADD
# am['mul'] = MULT
# am['div'] = DIV

# y = am(3, 4, 5, 6)
# print(y)

# # statement = 'and(a,b): c=f(x) /: or(a,b): c=f(y)'
# statement = 'and(a,b): x / none'
# function = Function(statement, ['a', 'b', 'c', 'd'])

# function['a'] = 1
# function['b'] = 1
# function['c'] = 0
# function['d'] = 0
# function['none'] = None

# function['x'] = 'or(c,d): f(y) / f(z)'
# function['y'] = -10
# function['z'] = 10

# function['and'] = AND
# function['or'] = OR
# function['f'] = ID

# y = function(1,1, 0,0)
# print(y)

# # from lib.data import *
# # from template import *
# # from templates.buffer import *
# # from templates.ordering import *
# # from templates.classifier import *


# # template = Buffer(4)
# # print(template(3), template['state data'])
# # print(template(3), template['state data'])
# # print(template(3), template['state data'])
# # print(template(3), template['state data'])
# # print(template(3), template['state data'])
# # print(template(3), template['state data'])


# # x = ['a', 'b', 'c', 'd', 'e']
# # o = Ordering(x)
# # o.order('a', 'b')
# # o.order('b', 'c')
# # o.order('c', 'a')
# # print(o('a', 'b'))

# # c = Classifier(execute(str.upper, x))
# # c.assign('a', 'A', 'B', 'C', 'D')
# # c.assign('b', 'B', 'C', 'D')
# # c.assign('c', 'C', 'A', 'E')
# # c.assign('d', 'D', 'E')
# # c.assign('e', 'E')

# # print(c)
