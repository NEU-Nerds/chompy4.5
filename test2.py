# import util
def layerEquivalence(path):
		layerEq = [False] * len(path)
		for i in range(1, len(path)):
			layerEq[i] = path[i] == path[i-1]
		return layerEq

def getP(p, pM, dM):
	lE= layerEquivalence(p)
	# print(f"lE: {lE}")
	if p[0] > pM:
		yield from recP(list(p)[:], lE, True, 1)
	for x in range(max(p[0],pM+1), pM+dM+1):
		# print(f"x: {x}")
		wP = list(p)[:]
		wP[0] = x
		if x != p[0]:
			yield tuple(wP)
		yield from recP(wP, lE, False, 1)



def recP(wP, lE, untouched, i):
	# untouched = copy(untouched)
	wP = wP[:]
	# print(f"RecP call with: {wP}, {lE}, {untouched}, {i}")
	if i >= len(wP):
		# print("HELLO")
		return


	# if i < len(wP)-1 or not untouched:
	yield from recP(wP, lE, untouched, i+1)

	# for i in range(startI, len(wP)):
		# yield from recP(wP, i+1)
	if untouched:
		untouched = False
		for x in range(wP[i]+1, wP[i-1]+1):
			wP[i] = x
			# print(f"yielding {wP}")
			yield tuple(wP)
			yield from recP(wP, lE, untouched, i+1)
	elif lE[i]:
		# print("HI")
		untouched = False
		for x in range(wP[i]+1, wP[i-1]+1):
			wP[i] = x
			# print(f"yielding {wP}")
			yield tuple(wP)
			yield from recP(wP, lE, untouched, i+1)




# pM = 6
#
# evenNode = (4, 4, 4, 3, 3, 3, 2)

# for i in range(1, 5):
# 	print(f"\nparents of: {evenNode}\npM: {pM}\ndM: {i}")
# 	l = list(util.getParentsTest(pM, i, evenNode))
# 	l.sort()
# 	print(l)
s = 0
d = 0
allP = set()
for parent in getP((2,2,1), 2,1):
	print(f"parent: {parent}")
	s += 1
	if parent in allP:
		d+= 1
	else:
		allP.add(parent)
print(d/s)
print(s)
