import util
import os
from pathlib import Path
import time


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
# THIS_FOLDER = "/Users/tymarking/Documents/chomp/chompy4"
# print(THIS_FOLDER)
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")
EVENS_FOLDER = Path(DATA_FOLDER, "./evens")

MAX_M = 5
MAX_N = 5

DELTA_N = 1
DELTA_M = 1

def main():

	#load roots
	m, n = util.load(DATA_FOLDER / "mXn.dat")
	roots = util.load(DATA_FOLDER / "roots.dat")
	print("loaded")
	# print(f"m: {m}")
	# print(f"n: {n}")

	#load m,n

	while m < MAX_M or n < MAX_N:
		dM = min(DELTA_M, MAX_M - m)
		dN = min(DELTA_N, MAX_N - n)
		# print(f"m: {m}")
		# print(f"n: {n}")
		# print(f"dM: {dM}")
		# print(f"dN: {dN}")
		sT = time.time()

		#expand sideways by dM
		# print(f"roots: {roots}")
		roots.update(util.expandSide(EVENS_FOLDER, m, n, dM, dN))
		# print(f"roots: {roots}")
		#expand down by dN
		evens, roots = util.expandDown(roots, m, n, dM, dN)

		endT = time.time()

		m += dM
		n += dN

		# sumEvens = len(evens)
		allEvens = set()

		for x in range(1,n):
			eX = util.load(EVENS_FOLDER / f"evens{x}.dat")
			allEvens.update(eX)
		allEvens.update(evens)

		print(f"{m}X{n} #total evens: {len(allEvens)}\t in {str(endT-sT)}s")
		print(str(n)+"X"+str(n)+" evens: " + str(allEvens))


		#store this depth's evens evens
		util.store((m,n), DATA_FOLDER / "mXn.dat")
		util.store(evens, EVENS_FOLDER / f"evens{n}.dat")
		util.store(roots, DATA_FOLDER / "roots.dat")


def seed():
	roots = set()
	evens = set([(1,)])

	try:
		os.mkdir(Path(THIS_FOLDER, "./data"))
	except:
		pass
	try:
		os.mkdir(DATA_FOLDER)
	except:
		pass
	try:
		os.mkdir(EVENS_FOLDER)
	except:
		pass

	util.store((1,1), DATA_FOLDER / "mXn.dat")
	util.store(roots, DATA_FOLDER / "roots.dat")
	util.store(evens, EVENS_FOLDER / "evens1.dat")



if __name__ == '__main__':
	seed()
	main()
