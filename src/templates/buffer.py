from lib.template import *
from lib.util import *

def APPEND(X):
	x = X[0]
	M = X[1]
	if identify(M) == 'list':
		M.append(x)
	else:M = [x]
	return M

def EXEC(X):
	f = X[0]
	y = []
	for x in X[1:]:
		y.append(f(x))
	return y

def SIZE_CONDITION(X):
	return len(X[0]) >= X[1]

def CONDITIONAL_RESET(X):
	if X[0]: return type(X[1])()
	else: return X[1]

def AND(X):
	return X[0] and X[1]

def PAIRED_EXEC(X):
	y = []
	f = X[0]
	for i in range(1, len(X)-1):
		y.append(f([X[i], X[i+1]]))
	return y

def signature(input_type, output_type):
	return Dictionary({'input type': input_type, 'output type': output_type})

SIGNATURES = Dictionary({
	'APPEND':signature(['*', 'list'], 'list'),
	'SIZE_CONDITION':signature(['list', 'int'], 'bool'),
	'CONDITIONAL_RESET':signature(['bool', '*'], '*'),
})

def Buffer(buffer_size):
	template = Template()
	template + ('append', [APPEND, ['input data', 'memory data'], 'memory data'])
	template + ('condition', [SIZE_CONDITION, ['memory data', buffer_size], 'state data'])
	template + ('reset', [CONDITIONAL_RESET, ['state data', 'memory data'], 'memory data'])
	template + ('output', [ID, 'memory data', 'output data'])
	template + ('function list', ['reset', 'append',  'output', 'condition'])
	return template

