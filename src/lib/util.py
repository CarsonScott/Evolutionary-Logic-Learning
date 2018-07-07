from goodata import Dict
from lib.types import *
from lib.functions import *
import numpy as np
from random import randrange as rr
import utilities
import math 


def random_str(size):
	x = list('abcdefghijklmnopqrstuvwxyz')
	y = ''
	done = False
	while not done:
		c = x[rr(len(x))]
		del x[x.index(c)]
		y += c
		if len(y) == size or len(x) == 0:
			done = True
	return y


def tanh(x):return math.tanh(x)
def pos_tanh(x):return (1 + tanh(x)) * 0.5
def neg_tanh(x):return (tanh(x) - 1) * 0.5

def softmax(x):
	return math.log(1 + np.exp(x))
def logistic(x):
	  return 1 / (1 + np.exp(-x))
def gaussian(x, height=1, center=0, deviation=1):
	return height * np.exp(- np.power(x-center, 2) / np.power(2*deviation, 2))
	
def sort(d):
	if isinstance(d, Dict):
		keys = list(d.keys())
	elif isinstance(d, list):
		keys = [i for i in range(len(d))]

	K = []
	X = []
	for k in keys:
		if d[k] != None:
			K.append(k)
			X.append(d[k])
	keys = K
	vals = X

	if len(keys) <= 1:
		return keys

	done = False
	while not done:
		done = True
		for i in range(len(keys)-1):
			k1 = keys[i]
			k2 = keys[i+1]

			v1 = vals[i]
			v2 = vals[i+1]

			if v2 < v1:
				done = False
				keys[i] = k2
				vals[i] = v2
				keys[i+1] = k1
				vals[i+1] = v1
	return keys


def reverse(X):
	Y = []
	for i in range(len(X)-1, -1, -1):
		Y.append(X[i])
	return Y

# Database for translating keys into functions and vice-versa 
FUNCTIONS = Dict({'appear':APP, 'disappear':DIS, 'increase':INC, 'decrease':DEC, 'change':DIF})
TYPES = Dict({'bool':['appear', 'disappear'], 'int':['increase', 'decrease'], 'float':['increase', 'decrease'], 'other':['change']})
CONSTRUCTORS = Dict({'bool':BOOL, 'int':INT, 'float':FLOAT, 'string':STRING, 'list':LIST, 'dict':DICT})

# Instantiate a given type to form an object
def create(T):
	if T in CONSTRUCTORS.keys():
		return CONSTRUCTORS[T]()

	# Y = Type()
	# for i in range(len(T)):
	# 	t = T[i]
	# 	y = None
	# 	if isinstance(t, Type):
	# 		y = create(t)
	# 	elif t in CONSTRUCTORS.keys():
	# 		c = CONSTRUCTORS[t] 
	# 		y = c()
	# 	Y.append(y)
	# return Y