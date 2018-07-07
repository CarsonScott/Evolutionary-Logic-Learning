from types import *

def union(A, B):
    Y = []
    for x in A+B:
        if x not in Y:
            Y.append(x)
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
    for i in range(len(B)):
        b = B[i]
        if b not in A:
            Y.append(b)
    return Y

def equivalent(A, B):
    return len(compliment(A, B)) == 0 and len(compliment(B, A)) == 0
def containment(A, B):
    return not len(compliment(B, A))
def disjoint(A, B):
    return not len(intersection(A,B))
def conjoint(A, B):
    return not disjoint(A,B)