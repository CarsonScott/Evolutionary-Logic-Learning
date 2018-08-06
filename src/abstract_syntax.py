from control_flow import *

class AbstractSyntax(PathSelector):
	def __init__(self):
		super().__init__()

keys = ['statement', 'open', 'close', 'lefthand', 'righthand', 'relation']

ast = AbstractSyntax()
ast.set_objects(keys, keys)
ast.set_function(random_choice)
ast.set_path('statement', 'open')
ast.set_path('open', 'lefthand')
ast.set_path('lefthand', 'relation')
ast.set_path('righthand', 'relation')
ast.set_path('relation', 'righthand')
ast.set_path('righthand', 'close')
ast.set_path('close', 'statement')
ast.set_state('statement')


variables = list('abcdefghijklmnopqrstuvwxyz'.upper())
relations = [' ~> ', ':']
assignments = []
string = ''
for i in range(100):
	y = ast()[0]
	x = None
	if y == 'lefthand' or y == 'righthand':
		options = compliment(assignments, variables)
		x = options[rr(len(options))]
		assignments.append(x)
	if y == 'relation':
		x = relations[rr(len(relations))]
	if y == 'open':
		x = '('
	if y == 'close':
		x = ')'

	if x != None:
		string += x
	else:
		print(string)
		assignments = []
		string = ''
