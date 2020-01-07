import util

"""
f = "4-3-3-2.dat"
prefix = []
c = 0
while c < len(f) and f[c] != ".":
	prevC = c
	while c < len(f) and f[c] != "." and f[c] != "-":
		c += 1
	prefix.append(int(f[prevC:c]))
	if f[c] == ".":
		break
	else:
		c += 1
print(prefix)
"""
even = (2, 2, 2, 1)
pM = 2
dM = 2
parents = util.getParents(pM, dM, even)
print(f"even: {even}")
print(f"pM: {pM}\t dM: {dM}")
print(f"parents: {parents}")
