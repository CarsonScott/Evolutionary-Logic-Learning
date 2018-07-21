from lib.data import *
from matrix import *
from script.expresol.Language import *

class Script(Matrix):
	def load(self, file):
		data = load(file, '.txt')
		self = Script(data)
		return self
	def save(self, file):
		data = Matrix(self)
		save(data, file, '.txt')


metalogic = System()



# from xml.etree.ElementTree import *
# y = ElementTree(file='test.xml')
# c = y.getroot()
# to = y.find('to').text
# print(to)
# print(y.find('from').text)
