from lib.util import *

class Detector(Dict):
	def __init__(self, X):
		self.previous = None
		self.current = X
		self.update(X)

	def update(self, X):
		self.current = X
		deltas = Dict()
		if self.previous == None:
			self.previous = Dict()
			for i in self.current.keys():
				self.previous[i] = self.current[i]
		else:
			for i in self.current.keys():
				Xi = self.previous[i]
				Xf = self.current[i]
				y = detect([Xi, Xf])
				self.previous[i] = Xf
				deltas[i] = y
		return deltas
	
# Assign labels that indicate how a variable changed over time 
def detect(X):
	Xi = X[0]
	Xf = X[1]
	if not compare(Xi, Xf):
		error = 'inconsistent data types (' 
		error += str(identify(Xi)) + ', ' 
		error ++ str(identify(Tf)) + ')'
		raise Exception(error)
	F = TYPES[identify(Xi)]
	Y = []
	for i in F:
		f = FUNCTIONS[i]
		if f([Xi, Xf]):
			Y.append(i)
	return Y

class DetectorSystem(Dict):
	def __init__(self):
		self.detector = None

	def __call__(self):
		if self.detector == None:
			self.detector = Detector(self)
		else:return self.detector.update(self)


ds = DetectorSystem()
ds['a'] = True
ds['b'] = False
ds['c'] = 0.3
ds()

ds['a'] = False
ds['b'] = True
ds['c'] = 0.5

y = ds()

print(y)


# X  = Dict({'a':False})
# detector = Detector(X)

# X['a'] = True
# Y = detector.update(X)
# print(Y)