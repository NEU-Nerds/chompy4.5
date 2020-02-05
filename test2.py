import time


b1 = [17,16,16,16,15,14,14,14,13,13,12,6,6,7,4,4,2]

t1 = time.time()
n = 10**4
for i in range(n):
	getConjugate(b1)
print(f"Avergage time: {(time.time()-t1)/n}")
# print(f"conjugate of {b1} = {getConjugate(b1)}")
