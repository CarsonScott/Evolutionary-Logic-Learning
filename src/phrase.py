from lib.util import *

PHRASES = Dict({
	'PP': ['/P/', '/N'],	# Prepositional Phrase
	'AP': ['/A/', '/N'],	# Adjective Phrase
	'DP': ['/D/', '/N'],	# Determiner Word
	'NP': ['/N/', 'DP']		# Noun Phrase
})

class OrderedDict(Dict):
	def __init__(self):
		self.ranks = Dict()
	def set_rank(self, key, rank):
		self.ranks[key] = rank
	def get_rank(self, key):
		return self.ranks[key]
	def sort(self):
		return sort(self.ranks)
	def index(self):
		output = []
		for i in self.keys():
			output.append(self.ranks[i])
		return output

class Phrase(Dict):
	def __init__(self, key=None):
		self['type'] = None
		self['head'] = None
		self['vars'] = []
		self['data'] = []
		self['reqs'] = []
		self['nest'] = []
		if key != None:
			self.create(key)

	def get_required(self):
		output = []
		variables = self['vars']
		requirements = self['reqs']
		for i in range(len(requirements)):
			if requirements[i]:
				output.append(variables[i])
		return output

	def get_assigned(self):
		output = []
		variables = self['vars']
		data = self['data']
		for i in range(len(data)):
			if data[i] != None:
				output.append(variables[i])
		return output

	def get_nested(self):
		output = []
		variables = self['vars']
		for i in range(len(variables)):
			nested = self['nest'][i]
			if nested:output.append(variables[i])
		return output

	def set_value(self, element, value):
		index = self['vars'].index(element)
		self['data'][index] = value

	def get_value(self, element):
		index = self['vars'].index(element)
		return self['data'][index]

	def is_valid(self):
		required = self.get_required()
		assigned = self.get_assigned()
		return containment(required, assigned)

	def create(self, key, memory=PHRASES):
		if key in memory.keys():
			phrase = memory[key]
			self['type'] = key
			for i in range(len(phrase)):
				word = phrase[i]
				data = None
				required = False
				header = False
				nested = False
				if word[0] == '/':
					required = True
					if word[len(word)-1] == '/':
						header = True
						word = word[:len(word)-1]	
					word = word[1:]
				if word in memory.keys():
					if word != key:
						nested = True
				if header:self['head'] = word
				self['vars'].append(word)
				self['data'].append(data)
				self['reqs'].append(required)
				self['nest'].append(nested)
			return self

	def convert(self):
		output = OrderedDict()
		for i in range(len(self['vars'])):
			variable = self['vars'][i]
			output[variable] = self['data'][i]
			output.set_rank(variable, i)
		return output

	def translate(self):
		output = []
		data = self.convert()
		ordered = data.sort()
		for i in range(len(ordered)):
			output.append(data[ordered[i]])
		return output


	#############################
	### Phrase Structure Test ###
	#############################

# Create a noun phrase
y = Phrase('NP')

# Assign words to the determiner and noun slots
y.set_value('DP', 'happy')
y.set_value('N', 'dog')

# Analyze the phrase structure
nested = y.get_nested()			# A subset of elements that are also phrases, and therefore hierarchical
assigned = y.get_assigned()		# A subset of elements that are assigned to data, and are therefore satisfied
required = y.get_required()		# A subset of elements that are necessary to be assigned, and are therefore required
converted = y.convert()			# A dictionary representation of the phrase structure
translated = y.translate()		# A list representation of the phrase structure


print('nested:		' + str(nested) + '\nassigned:	' +  str(assigned) + '\nrequired:	' +  str(required))
print('\nconverted:	' + str(converted) + '\ntranslated:	' +  str(translated) + '\n')	

def phrase_tree(data, memory=PHRASES):
	if isinstance(data, str):
		phrase = Phrase(data)
	elif isinstance(data, Phrase):
		phrase = data

	nested = phrase.get_nested()
	output = phrase.convert()
	if len(nested) > 0:
		for i in range(len(nested)):
			key = nested[i]
			index = phrase['vars'].index(key)
			required = phrase['reqs'][index]
			subphrase = phrase_tree(Phrase(key))
			output[key] = subphrase 
			
	return output

T = phrase_tree('NP')

print(T)