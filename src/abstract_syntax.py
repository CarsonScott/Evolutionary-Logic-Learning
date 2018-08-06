from control_flow import *

class AbstractSyntax(PathSelector):
	def __init__(self):
		super().__init__()
		keys = ['statement', 'open', 'close', 'lefthand', 'righthand', 'relation']
		self.set_objects(keys, keys)
		self.set_path('statement', 'open')
		self.set_path('open', 'lefthand')
		self.set_path('lefthand', 'relation')
		self.set_path('righthand', 'relation')
		self.set_path('relation', 'righthand')
		self.set_path('righthand', 'close')
		self.set_path('close', 'statement')
		self.set_state('statement')

	def parse(self, statement):
		s = list(statement.split(' '))
		if self.has(statement):
			return self[statement]
		if '-->' in s:
			i = s.index('-->')
			left_hand = s[0:i]
			right_hand = s[i+1:len(s)]
			left_hand = merge('', left_hand)
			right_hand = merge('', right_hand)

			left_hand =self.parse(left_hand)
			right_hand =self.parse(right_hand)
			
			return left_hand, right_hand
		return


ast = AbstractSyntax()
ast.set_function(random_choice)
variables = list('abcdefghijklmnopqrstuvwxyz')
ast.set_objects(variables, variables)

relations = [' --> ']
assignments = []
assigned = []
string = ''

for i in range(500):
	y = ast()[0]
	x = None
	if y == 'lefthand' or y == 'righthand':
		options = compliment(assignments, variables)
		x = options[rr(len(options))]
		assignments.append(x)
	if y == 'relation':
		x = relations[rr(len(relations))]
	if y == 'open' or y == 'close':
		x = ''
	if x != None:
		string += x
	else:
		path = ast.parse(string)
		if path != None:
			if None not in path:
				ast.set_path(*path)
		assigned = union(assigned, assignments)
		assignments = []
		string = ''


for i in assigned:
	sources = ast.get_sources(i)
	if sources == None:sources = []
	targets = ast.get_targets(i)
	if targets == None:targets = []
	key = str(i)
	print('('+merge('.', sources)+') --> |' + key + '| --> ('+ merge('.', targets)+')')


print(ast.get_interface())
