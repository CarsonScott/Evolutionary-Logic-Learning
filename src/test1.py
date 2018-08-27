from dictionary import *
from functional_logic import *
from functional_language import *

class FUNCTION(type):pass
class ASSOCIATION(type):pass
def FunctionFrame(operator, inputs):
	f = Dictionary()
	f['operator'] = operator
	f['inputs'] = inputs
	return f
def RelationFrame(source, relation, target):
	f = Dictionary()
	f['source'] = source
	f['relation'] = relation
	f['target'] = target
	return f

def Translate(frame, memory):
# Replaces the variables in a frame with the corresponding values stored in a seperate context
	output = copy(frame)
	for i in frame.keys():
		data = frame[i]
		islist = True
		if not isinstance(data, list):
			data = [data]
			islist = False
		for j in range(len(data)):
			if isinstance(data[j], dict):
				data[j] = Translate(data[j], memory)
			elif isinstance(data[j], str):
				data[j] = memory[data[j]]
		if not islist:data = data[0]
		output[i] = data
	return output

def Classify(frame):
# Compares the variables in a frame to the keywords of each possible type to find one that's equivalent
	frame_keys = frame.keys()
	function_keys = FunctionFrame(None, None).keys()
	relation_keys = RelationFrame(None, None, None).keys()
	if contains(frame_keys, function_keys):return FUNCTION
	if contains(frame_keys, relation_keys):return ASSOCIATION

def Transform(frame):
# Computes an output value by arranging the variables in a frame in python based on the operational role of the type
	if Classify(frame) == ASSOCIATION:
		f = frame['relation']
		x = [frame['source'], frame['target']]
		return Transform(FunctionFrame(f, x))
	if Classify(frame) == FUNCTION:
		f = frame['operator']
		x = frame['inputs']
		return f(x)

def Express(frame):
# Represents a frame by a string that follows syntactic rules of a formal language
	y = str()
	if Classify(frame) == ASSOCIATION:
		s = frame['source']
		t = frame['target']
		r = frame['relation']
		x = [str(s), str(r), str(t)]
		for i in range(len(x)):
			y += x[i]
			if i != len(x)-1:
				y += ' '
	if Classify(frame) == FUNCTION:
		f = frame['operator']
		x = frame['inputs']
		y = str(f) + '('
		for i in range(len(x)):
			y += str(x[i])
			if i != len(x)-1:
				y += ','
		y += ')'
	return y

# Converts an expression to a frame
def Extract(expression):
	if '(' in expression:
		if ')' in expression:
			i = expression.index('(')
			j = expression.index(')')
			f = expression[0:i]
			x = expression[i+1:j].split(',')
			return FunctionFrame(f, x)
	elif ' ' in expression:
		if len(expression.split()) == 3:
			s,r,t = expression.split()
			return RelationFrame(s, r, t)
	print(expression)

def ADD(X):
	return sum(X)
def GT(X):
	x = X[0]
	for i in range(1, len(X)):
		if X[i] <= x:
			return False
	return True


def func(x):
	return x*2

F = Function('y=f(x)', ['x'])
F['a'] = 5
F['b'] = 6
F['c'] = 4
F['x'] = 3
F['y'] = 4
F['f'] = func
F['add'] = ADD
F['>'] = GT

print(f(4))

f = FunctionFrame('add', ['a', 'b', 'c'])
sf = Express(f)
yf = Transform(Translate(f,F))

r = RelationFrame('x', '>', 'y')
sr = Express(r)
yr = Transform(Translate(r,F))

print(sr, '\n', yr)
print(sf, '\n', yf)