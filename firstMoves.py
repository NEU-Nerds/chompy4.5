import util
# import heritage3
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/mainRun/")
# ETA_FOLDER = DATA_FOLDER / "etaData/"
#etaData = util.load(DATA_FOLDER / "etaData.dat")

def getChildren(state):
	children = []
	#print("State: " +str(state))
	bites = getChoices(state)
	#print("Choices: " + str(bites))
	for bite in bites:
		child = biteF(state, bite)
		#if util.getN(child) >= util.getM(child):
		children.append(child)
	return children

def biteF(b, pos):
	if pos[1] == 0:
		return b[:pos[0]]

	board = b[:]

	for row in range(pos[0], len(board)):
		if board[row] > pos[1]:
			board[row] = pos[1];
		else:
			break

	# board = [r if r > pos[1] else r for r in b]

	return board

def getChoices(board):
	choices = [(i, j) for i in range(len(board)) for j in range(board[i])]
	choices = choices[1:]
	return choices


n = 19
firstMoves = {}
evens = set()
for f in os.listdir(DATA_FOLDER / "evens"):
	print(f"Loading {f}")
	newEvens = util.load(DATA_FOLDER / f"evens/{f}")
	evens.update(newEvens)

# evens = set(n_evens[1])
for i in range(2,n+1):
	for j in range(i,n+1):
		print("Getting moves for " + str(i)+"X"+str(j))
		fms = []
		emptyB = [j]*i
		children = getChildren(emptyB)
		for child in children:
			#for children that are rectangles (may not show up in the right file)
			# if child[0] == child[-1]:
			# 	continue
			if tuple(child) in evens:
				fms.append(list(child))
		firstMoves[str(i)+"X"+str(j)] = fms
		if len(fms) > 1:
			print("Length of "+ str(i)+"X"+str(j)+" fms is " + str(len(fms)))
print(f"First moves: {firstMoves}")
util.storeJson(firstMoves, DATA_FOLDER / "firstMovesV4-5_19.json")
