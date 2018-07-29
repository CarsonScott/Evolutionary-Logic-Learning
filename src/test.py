from function_language import *

def ID(x):
	return x
def AND(x):
	for i in x:
		if not i:return False
	return True
def OR(x):
	for i in x:
		if i: return True
	return False

am = Automaton(['c = div(f,g)', 'b = add(d,e)', 'a = mul(b,c)'], ['d', 'e', 'f', 'g'], ['a', 'b', 'c', 'd'])
am + 'a b c d e f mul add div'.split(' ')
am['a'] = 0
am['b'] = 0
am['c'] = 0
am['d'] = 0
am['e'] = 0
am['f'] = 0
am['g'] = 0
am['add'] = ADD
am['mul'] = MULT
am['div'] = DIV

y = am(3, 4, 5, 6)
print(y)

# statement = 'and(a,b): c=f(x) /: or(a,b): c=f(y)'
statement = 'and(a,b): x / none'
function = Function(statement, ['a', 'b', 'c', 'd'])

function['a'] = 1
function['b'] = 1
function['c'] = 0
function['d'] = 0
function['none'] = None

function['x'] = 'or(c,d): f(y) / f(z)'
function['y'] = -10
function['z'] = 10

function['and'] = AND
function['or'] = OR
function['f'] = ID

y = function(1,1, 0,0)
print(y)

# from lib.data import *
# from template import *
# from templates.buffer import *
# from templates.ordering import *
# from templates.classifier import *


# template = Buffer(4)
# print(template(3), template['state data'])
# print(template(3), template['state data'])
# print(template(3), template['state data'])
# print(template(3), template['state data'])
# print(template(3), template['state data'])
# print(template(3), template['state data'])


# x = ['a', 'b', 'c', 'd', 'e']
# o = Ordering(x)
# o.order('a', 'b')
# o.order('b', 'c')
# o.order('c', 'a')
# print(o('a', 'b'))

# c = Classifier(execute(str.upper, x))
# c.assign('a', 'A', 'B', 'C', 'D')
# c.assign('b', 'B', 'C', 'D')
# c.assign('c', 'C', 'A', 'E')
# c.assign('d', 'D', 'E')
# c.assign('e', 'E')

# print(c)
