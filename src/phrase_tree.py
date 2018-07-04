from tree import *
from phrase_operators import *
from kernel import *

def tanh(x):return math.tanh(x)
def pos_tanh(x):return (1 + tanh(x)) * 0.5
def neg_tanh(x):return (tanh(x) - 1) * 0.5

class Trainer:
	def __init__(self, learning_rate=0.1):
		self.value = 0
		self.delta = 0
		self.lrate = learning_rate

	def __call__(self, target):
		rate = self.lrate
		delta = self.delta
		error = target - self.value
		delta = tanh(error)
		
		self.value += self.delta + delta
		self.delta += delta * (1 - tanh(abs(self.delta)))
		if self.delta < 0:
			self.delta += rate * (1 + tanh(abs(self.delta)))
			if self.delta > 0: self.delta = 0
		if self.delta > 0:
			self.delta -= rate * (1 + tanh(abs(self.delta)))
			if self.delta < 0: self.delta = 0
		return self.value

trainer = Trainer()

lo, hi = 60, 65

px = None
x = rr(-100, 100)
step = 100
for i in range(10000):
	if i % 200 == 0:
		step = rr(1, 55)
		x = x + rr(-step, step)
	y = trainer(x)
	print(str(i) + '	' + str(x) + '	' + str(y))
	px = x

# pt.display()

# fitness = pt.update()
# print(fitness)