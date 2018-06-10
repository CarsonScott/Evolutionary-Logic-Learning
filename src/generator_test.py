from Generator import * 

G2 = Generator(5, f1)
for i in range(1000):
	print(G2(i))
# # g = FunctionGenerator(2)
# # g['and'] = AND
# # g['x'] = True
# g['y'] = False
# g['a'] = False
# g['b'] = False
 
# X = ['and', 'x', 'y', 'and', 'a', 'b']
# for i in range(len(X)):
# 	f = g(X[i])
# print(g['data'])