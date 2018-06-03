from types import *

def union(A, B):
    Y = list(A)
    for b in B:
    	if b not in Y:
    		Y.append(b)
    return Y
def intersection(A, B):
    Y = list()
    for i in range(len(A)):
        a = A[i]
        if a in B:
            Y.append(a)
    return Y
def compliment(A, B):
    Y = list()
    for i in range(len(A)):
        a = A[i]
        if a not in B:
            Y.append(a)
    return Y

def equivalent(A, B):
    return not len(compliment(A, B)) and not len(compliment(B, A))
def containment(A, B):
    return not len(compliment(B, A))
def disjoint(A, B):
    return not len(intersection(A,B))
def conjoint(A, B):
    return not disjoint(A,B)