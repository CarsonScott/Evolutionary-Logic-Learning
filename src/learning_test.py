from motivator import *
from recognizer import *

p = [
	Proposition('(0 | 0);'),
	Proposition('(1 | 1);'),
	Proposition('(2 | 2);'),
	Proposition('(3 | 3);'),
	Proposition('(4 | 4);')]
m = Motivator(p, 1)

X = [
	{'0': True,'1': False,'2': False,'3': False, '4':False},
	{'0': False,'1': True,'2': False,'3': False, '4':False},
	{'0': False,'1': False,'2': False,'3': False, '4':False},
	{'0': False,'1': False,'2': True,'3': False, '4':False},
	{'0': False,'1': False,'2': False,'3': True, '4':False},
	{'0': False,'1': False,'2': False,'3': False, '4':True}]

# for i in range(len(X)):
# 	for j in range(1):
# 		X.insert(i, {'0': False,'1': False,'2': False,'3': False, '4':False})

r = Recognizer([0, 0, 0, 0, 0], 10, 0.002, 0.0001)

def to_dict(x):
	d = Dict()
	for i in range(len(x)):
		d[str(i)] = x[i]
	return d

log = open('log.txt', 'w')
m.set_goal(4)
c = -1
for i in range(7000):
	for x in X:
		c += 1
		y = m.compute(x)

		g = []
		for j in range(len(y)):
			if y[j] > 0:
				g.append(str(i))

		s = str(c) + '	'
		for j in y:
			s += str(j) + '	'

		# s +'			' + str(p)	
		if i % 10 == 0:
			log.write(s+'\n')
		print(s)
	print()

log.close()