from model_memory import *

class FunctionMemory(PatternMemory):
	def construct(self, data):
		data = self.translate(data)
		model = Model(data)
		return model

	def identify(self, data):
		if isinstance(data, Model):
			return 'model'
		return super().identify(data)

	def convert(self, key):
		self[key] = self.construct(key)

	def __call__(self, data):
		if self.identify(self.translate(data)) == 'pattern':
			data = self.translate(data)
			if self.identify(self.translate(data[0])) == 'model':
				f = self.translate(data[0])
				x = self.translate([data[i] for i in range(1, len(data))])
				y = f(x)
				return y

mem = FunctionMemory()
mem['a'] = ('^', 'b', 'c')
mem['b'] = 5
mem['c'] = 3
mem['d'] = 3
mem.convert('a')

y = mem(('a', 'b', 'd'))
print(y)