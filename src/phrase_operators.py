from lib.util import *
from lib.relations import *

def key_operation(p1, p2, function):
	k1 = list(p1.keys())
	k2 = list(p2.keys())
	return function(k1, k2)
def key_intersection(p1, p2):
	return key_operation(p1, p2, intersection)
def key_compliment(p1, p2):
	return key_operation(p1, p2, compliment)
