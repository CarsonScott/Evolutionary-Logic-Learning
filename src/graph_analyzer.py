from lib.util import *
from kernel import *

class Space(list):
	def __init__(self, data=None, step=1):
		self.angles = []
		self.positions = []
		self.step = step
		if data != None:
			for x in data:
				self.append(x)
	def append(self, value, step=None):
		if step == None:
			step = self.step

		new_position = 0
		prev_value = 0
		if len(self) > 0:
			prev_value = self[len(self)-1]
			dx = self.step
			dy = value - prev_value
			angle = math.atan2(dy, dx) 
			self.angles.append(angle)
			prev_position = self.positions[len(self.positions)-1]
			new_position = prev_position + step

		self.positions.append(new_position)
		super().append(value)

	def sort(self):
		positions = self.positions
		values = list(self)
		indices = sort(positions)
		step = self.step

		self = Space()
		for i in range(len(values)):
			j = indices[i]
			x = values[j]
			p = positions[j]

			if i != 0:
				step = p - self.positions[i-1]
			self.append(x, step)

	def get(self, index):
		x = self.positions[index]
		y = self[index]
		return x,y

def display(space):
	for i in range(len(space)):
		x,y = space.get(i)
		print(str(x) + '	' + str(y))

def organize(values, indices):
	output = [None for i in range(len(values))]
	for i in range(len(values)):
		x = values[i]
		j = indices[i]
		output[j] = x
	return output

space = Space()
for i in range(-5, 5):
	x = gaussian(i)
	space.append(x)
	print(space)

space.sort()
kernel = Kernel('mean')
kernel1 = Kernel('max')
kernel2 = Kernel('min')

x = space
y = kernel(x, 2, 2)
a = space.angles


display(space)

print(x, '\n', a)

# space1 = Space(y)
# x1 = space1
# a1 = space1.angles

# print('\n', x, '\n', a)
# print('\n', x1, '\n', a1)
