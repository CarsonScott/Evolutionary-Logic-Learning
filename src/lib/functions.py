
# ------------- DETECTION FUNCTIONS ------------- #

def INC(X):
	Xi = X[0]
	Xf = X[1]
# detects an increase in numerical value  
	return Xi < Xf
def DEC(X):
	Xi = X[0]
	Xf = X[1]
# detects a decrease in numerical value 
	return Xi > Xf
def APP(X):
	Xi = X[0]
	Xf = X[1]
# detects a boolean value becoming true
	return not Xi and Xf
def DIS(X):
	Xi = X[0]
	Xf = X[1]
# detects a boolean value becoming false
	return Xi and not Xf
def DIF(X):
	Xi = X[0]
	Xf = X[1]
# detects any other kind of value changing
	return Xi != Xf


# -------------- LOGICAL FUNCTIONS -------------- #

def NOT(X):
# negates a boolean value
	return not X
def AND(X):
	Xi = X[0]
	Xj = X[1]
# measures a conjunction between two boolean values
	return Xi and Xj
def OR(X):
	Xi = X[0]
	Xj = X[1]
# measures a disjunction between two boolean values
	return Xi or Xj


# ------------ COMPARATIVE FUNCTIONS ------------ # 

def LT(X):
	Xi = X[0]
	Xj = X[1]
# checks if one value is less than another
	return Xi < Xj
def GT(X):
	Xi = X[0]
	Xj = X[1]
# checks if one value is greater than another
	return Xi > Xj
def EQ(X):
	Xi = X[0]
	Xj = X[1]
# checks if one value is equal to another
	return Xi == Xj
def LTE(X):
	Xi = X[0]
	Xj = X[1]
# checks if one value is less than or equal to another
	return Xi <= Xj
def GTE(X):
	Xi = X[0]
	Xj = X[1]
# checks if one value is greater than or equal to another
	return Xi >= Xj
def IN(X):
	Xi = X[0]
	Xj = X[1]
# checks if one value exists within a set
	return Xi in Xj
def NIN(X):
	Xi = X[0]
	Xj = X[1]
# checks if one value does not exist within a set
	return NOT(IN(X))

def ADD(X):
	Xi = X[0]
	Xj = X[1]
	return Xi + Xj
def SUB(X):
	Xi = X[0]
	Xj = X[1]
	return Xi - Xj
def MULT(X):
	Xi = X[0]
	Xj = X[1]
	return Xi * Xj
def DIV(X):
	Xi = X[0]
	Xj = X[1]
	if Xj != 0:
		return Xi / Xj

# class Function:
# 	def __init__(self, operator, inputs, defaults=dict()):
# 		self.function = operator
# 		self.max_size = inputs
# 		self.constant = {}

# 		for i in range(self.max_size):
# 			self.constant[i] = None
# 			if i in defaults.keys():
# 				self.constant[i] = defaults[i]

# 		for i in range(self.max_size):
# 			if i not in self.constant.keys():
# 				self.constant[i] = None

# 	def __call__(self, inputs):
# 		L = dict()
# 		for i in range(self.max_size):
# 			if self.constant[i] != None:
# 				L[i] = self.constant[i]
# 			elif i in range(0, len(inputs)):
# 				L[i] = inputs[i]
		
# 		X = list()
# 		for i in range(self.max_size):
# 			value = L[i]
# 			X.append(value)
# 		F = self.function
# 		return F(X)

# class Store:
# 	def __init__(self, world, index, value):
# 		self.world = world
# 		self.index = index
# 		self.value = value
# 	def __call__(self, X):
# 		i = self.world
# 		j = self.index
# 		x = self.value 
# 		X[i][j] = x
# 		return X

# class Retrieve:
# 	def __init__(self, world, index):
# 		self.world = world
# 		self.index = index
# 	def __call__(self, X):
# 		i = self.world
# 		j = self.index
# 		return X[i][j] 