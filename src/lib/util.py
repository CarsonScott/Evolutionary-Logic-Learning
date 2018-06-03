from goodata import Dict
from lib.types import *
from lib.functions import *
from random import randrange as rr

def sort(d):
    if isinstance(d, dict):
        keys = list(d.keys())
    elif isinstance(d, list):
        keys = [i for i in range(len(d))]

    vals = []
    for i in range(len(keys)):
        k = keys[i]
        vals.append(d[k])

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