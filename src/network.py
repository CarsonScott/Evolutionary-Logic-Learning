from lib.util import *


class Network:
	def __init__(self, nodes):
		self.nodes = []
		if isinstance(nodes, dict):
			self.nodes = Dict(nodes)
			for i in self.nodes.keys():
				self.nodes[i] = Dict(nodes)
				for j in self.nodes[i].keys():
					self.nodes[i][j] = 0
		elif isinstance(nodes, int):
			self.nodes = [[0 for i in range(nodes)] for j in range(nodes)]

	def add(self, key, value=0):
		if key not in self.nodes.keys():
			self.nodes[key] = Dict(self.nodes.keys() + [key])
			for i in self.nodes[key].keys():
				self.nodes[key][i] = value

	def train(self, active, rate):
		for i in active:
			for j in active:
				self.nodes[i][j] += rate

def print_network(network):
	string = ''

	if isinstance(network.nodes, list):
		for i in range(len(network.nodes)):
			string += str(i) + '\n'
			for j in range(len(network.nodes[i])):
				string += '	' + str(j) + ': ' + str(network.nodes[i][j]) + '\n'
	elif isinstance(network.nodes, Dict):
		for i in network.nodes.keys():
			string += str(i) + '\n'
			for j in network.nodes[i].keys():
					string += '	' + str(j) + ': ' + str(network.nodes[i][j]) + '\n'

	print(string)