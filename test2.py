import time

def getChildren(node):
	node = list(node)
	for i in range(len(node)):
		if i != 0:
			yield tuple(node[:i])
		for j in range(1, node[i]):
			# if i == 0 and j == 0:
			# 	continue
			#"biting" at i,j
			ret = node[:]
			nI = i
			while nI < len(node) and node[nI] > j:
				ret[nI] = j
				nI += 1
			yield tuple(ret)

b1 = [17,16,16,16,15,14,14,14,13,13,12,6,6,7,4,4,2]
b2 = [3,2,1]
t1 = time.time()
n = 10**7
for i in range(n):
	getChildren(b2)
print(f"Avergage time: {(time.time()-t1)/n}")
# print(f"conjugate of {b1} = {getConjugate(b1)2}")
# cs = getChildren(b1)
# print(f"children of {b1}:")
# for c in cs:
# 	print(c)
