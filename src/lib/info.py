from relations import *
from functions import *
from goodata import Dict

C = {'and':AND, 'or':OR, 'not':NOT}
F = {'union':union, 'compliment':compliment, 'intersection':intersection}
R = {'equivalent':equivalent, 'containment':containment, 'disjoint':disjoint, 'conjoint':conjoint}

def Fun(A, f, B):
	f = F[f]
	return f(A,B)
def Rel(A, r, B):
	r = R[r]
	return r(A,B)
def assign(A, B):
	for key in R.keys():
		r = R[key]
		if r(A,B): return key
def state(terms):
	S = ''
	for x in terms:
		S += str(x) + ' '
	S + '.'
	return S
def parse(statement):
	T = statement.split(' ')
	M = ['.', '']
	I = intersection(T, M)
	while len(I) > 0:
		i = I[0]
		del T[T.index(i)]
		del I[I.index(i)]
	return T
def assign(terms):
	types = []
	for term in terms:
		if term in F.keys():
			t = 'function'
		elif term in R.keys():
			t = 'relation'
		elif term in C.keys():
			t = 'connective'
		else:
			t = None
		types.append(t)
	return types

def rank(X):
	U = []
	for x in X:
		U = union(U, x)
	R = Dict()
	for x in U:
		R[x] = 0

	for x in X:
		for i in R.keys():
			if i in x:
				R[i] += 1/len(X)
	return R

X = [
	['a', 'b', 'c'],
	['a', 'b'],
	['a']
]

print(rank(X))
statement = 'c conjoint b'
terms = parse(statement)
labels = assign(terms)

print(labels)
