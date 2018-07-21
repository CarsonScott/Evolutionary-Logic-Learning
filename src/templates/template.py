from Dictionary import *
def ID(x):
	return x

class FunctionTemplate(Dictionary):
	def __init__(self):
		super().__init__()
		self + ['input data',
				'memory data',
				'output data',
				'state data']

		self + ['input function',
				'memory function',
				'output function',
				'state function',
				'function list']
		for key in self.arrange()['function']:
			self[key] = (ID, None)
		self['self'] = self

	def _input_data(self):
		return self['input data']
	def _memory_data(self):
		return self['memory data']
	def _output_data(self):
		return self['output data']
	def _state_data(self):
		return self['state data']

	def _input_function(self):
		return self['input function']
	def _memory_function(self):
		return self['memory function']
	def _output_function(self):
		return self['output function']
	def _state_function(self):
		return self['state function']

	def set_input_data(self, data):
		self['input data'] = data
	def set_memory_data(self, data):
		self['memory data'] = data
	def set_output_data(self, data):
		self['output data'] = data
	def set_state_data(self, data):
		self['state data'] = data

	def reset(self):
		self.__init__()

	def execute(self, function):
		if function in self:
			function = self[function]
		elif is_iterable(function):
			function = function

		F = [None, None, None]
		for i in range(len(function)):
			F[i] = function[i]
		
		f, x, t = F
		f = self.translate(f)
		x = self.translate(x)
		y = f(x)

		if t != None:self[t] = y
		return y

	def classify(self, key):
		if key in self:
			words = key.split(' ')
			if len(words) >= 2:
				return words[1]

	def arrange(self):
		keys = self.keys()
		objects = Dictionary()
		for i in keys:
			object_type = self.classify(i)
			if object_type not in objects:
				objects + (object_type, [])
			objects[object_type].append(i)
		return objects

	def call(self, functions):
		outputs = []
		for f in functions:
			outputs.append(self.execute(f))
		return outputs

	def __call__(self, data=None):
		if data != None:self.set_input_data(data)
		self.call(self['function list'])
		return self._output_data()