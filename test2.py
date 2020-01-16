import util


pM = 6

evenNode = (4, 4, 4, 3, 3, 3, 2)

for i in range(1, 5):
	print(f"\nparents of: {evenNode}\npM: {pM}\ndM: {i}")
	l = list(util.getParentsTest(pM, i, evenNode))
	l.sort()
	print(l)
