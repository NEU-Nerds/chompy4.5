import util
import os
from pathlib import Path
import time


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
# THIS_FOLDER = "/Users/tymarking/Documents/chomp/chompy4"
# print(THIS_FOLDER)
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")
EVENS_FOLDER = Path(DATA_FOLDER, "./evens/")
ROOTS_FOLDER = Path(DATA_FOLDER, "./rootBatches/")
ROOTS_BY_SIGMA_FOLDER = Path(DATA_FOLDER, "./rootsBySigma/")

MAX_M = 10
MAX_N = 10

DELTA_N = 1
DELTA_M = 1

def main():

	#load roots
	m, n = util.load(DATA_FOLDER / "mXn.dat")
	# roots = util.load(DATA_FOLDER / "roots.dat")
	util.emptyDir(DATA_FOLDER / "roots")
	print("loaded")
	# print(f"m: {m}")
	# print(f"n: {n}")

	#load m,n
	firstST = time.time()
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
		util.expandSide(DATA_FOLDER, m, n, dM, dN)
		sideTime = time.time()
		print("Side time: " + str(sideTime - sT) )
		# prevRoots = util.load(DATA_FOLDER / "roots/rootsBatch0.dat")
		util.emptyDir(DATA_FOLDER / "parents")
		util.emptyDir(DATA_FOLDER / "oldRoots")

		# numRootBatches = len(os.listdir(DATA_FOLDER / "roots"))
		# util.store(roots, DATA_FOLDER / f"roots/rootsBatch{numRootBatches}.dat")
		# print(f"roots: {roots}")
		#expand down by dN
		roots = util.expandDown(DATA_FOLDER, m, n, dM, dN)
		print("Down time: " + str( time.time() - sideTime))

		endT = time.time()

		m += dM
		n += dN

		allEvens = set()
		for x in range(1,n+1):
			eX = util.load(EVENS_FOLDER / f"evens{x}.dat")
			allEvens.update(eX)

		print(f"{m}X{n} #total evens: {len(allEvens)}\t in {str(endT-sT)}s")


		# print(str(m)+"X"+str(n)+" evens: " + str(allEvens))

		# print(f"{m}X{n} in {str(endT-sT)}s")

		#store this depth's evens evens
		util.store((m,n), DATA_FOLDER / "mXn.dat")
		# util.store(evens, EVENS_FOLDER / f"evens{n}.dat")
		# util.store(roots, DATA_FOLDER / "roots.dat")
	print(f"total time: {time.time() - firstST} ")

def seed():
	try:
		util.emptyDir(DATA_FOLDER)
	except:
		pass

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
	try:
		os.mkdir(DATA_FOLDER / "roots")
	except:
		pass
	try:
		os.mkdir(DATA_FOLDER / "oldRoots")
	except:
		pass
	try:
		os.mkdir(DATA_FOLDER / "parents")
	except:
		pass
	try:
		os.mkdir(DATA_FOLDER / "sideOldRoots")
	except:
		pass
	try:
		os.mkdir(DATA_FOLDER / "sideRoots")
	except:
		pass


	util.store((1,1), DATA_FOLDER / "mXn.dat")
	util.store(roots, DATA_FOLDER / "roots/rootsBatch0.dat")
	util.store(evens, EVENS_FOLDER / "evens1.dat")

if __name__ == '__main__':
	seed()
	main()
