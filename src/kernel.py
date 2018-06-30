from lib.util import *

def Mean(X):
	if len(X) == 0:
		return None
	return sum(X) / len(X)
def Max(X):
	if len(X) == 0:
		return None
	return max(X)
def Min(X):
	if len(X) == 0:
		return None
	return min(X)

KERNEL_FUNCTIONS = Dict({
	'mean':	Mean,
	'max':	Max,
	'min':	Min,
})

class Kernel:
	def __init__(self, function):
		self.function = None
		if isinstance(function, str):
			if function in KERNEL_FUNCTIONS.keys():
				self.function = KERNEL_FUNCTIONS[function]
		else:self.function = function
	def __call__(self, space, kernel=1, step=1):
		output = []
		length = len(space)
		index = None
		done = False
		while not done:
			if index == None:
				new_index = 0
			else:
				new_index = index + step
			if new_index > length:
				done = True
			else:
				final_index = new_index + kernel
				if final_index > length:
					done = True
				else:
					x = space[new_index:final_index]
					y = self.function(x)
					output.append(y)
					index = new_index
		return output
