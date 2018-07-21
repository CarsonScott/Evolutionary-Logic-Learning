from types import *

def union(A, B):
    Y = []
    for x in A+B:
        if x not in Y:
            Y.append(x)
    return Y
def intersection(A, B):
    Y = []
    for a in A:
        if a in B:
            Y.append(a)
    return Y
def compliment(A, B):
    Y = []
    for b in B:
        if b not in A:
            Y.append(b)
    return Y

def equivalent(A, B):
    return len(compliment(A, B)) == 0 and len(compliment(B, A)) == 0
def contains(A, B):
    return not len(compliment(A, B))
def disjoint(A, B):
    return not len(intersection(A,B))
def conjoint(A, B):
    return not disjoint(A,B)
