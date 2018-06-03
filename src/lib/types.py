TYPES = {'bool':['appear', 'disappear'], 'num':['increase', 'decrease'], 'other':['change']}

class Type(list):
	pass
	
# Check the type of a given object
def identify(X):
	t = type(X).__name__.lower()
	return t

# Check whether two objects have the same type 
def compare(Xi, Xf):
	return identify(Xi) == identify(Xf)

# constructors for primitive types
def DATA(t, v=None):
	try:
		return t(v)
	except:
		return t()

def BOOL(v=None):
	return DATA(bool, v)
def INT(v=None):
	return DATA(int, v)
def FLOAT(v=None):
	return DATA(float, v)
def STRING(v=None):
	return DATA(str, v)
def LIST(v=None):
	return DATA(list, v)
def DICT(v=None):
	return DATA(Dict, v)

# representation of an infinite number
def INF(x=1):
	y = 'inf'
	if x < 0:
		y = '-' + y
	else:
		y = '+' + y
	return y

# representation of an infinite set
def ALL(x=1):
	y = 'all'
	if x < 0:
		y = '!' + y
	return y