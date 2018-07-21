from lib.data import *
from template import *
from templates.buffer import *
from templates.ordering import *
from templates.classifier import *


template = Buffer(4)
print(template(3), template['state data'])
print(template(3), template['state data'])
print(template(3), template['state data'])
print(template(3), template['state data'])
print(template(3), template['state data'])
print(template(3), template['state data'])


x = ['a', 'b', 'c', 'd', 'e']
o = Ordering(x)
o.order('a', 'b')
o.order('b', 'c')
o.order('c', 'a')
print(o('a', 'b'))

c = Classifier(execute(str.upper, x))
c.assign('a', 'A', 'B', 'C', 'D')
c.assign('b', 'B', 'C', 'D')
c.assign('c', 'C', 'A', 'E')
c.assign('d', 'D', 'E')
c.assign('e', 'E')

print(c)
