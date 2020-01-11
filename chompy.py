import util
import os
from pathlib import Path
import time
import expand
import sys
# from objsize import get_deep_size

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
# THIS_FOLDER = "/Users/tymarking/Documents/chomp/chompy4"
# print(THIS_FOLDER)
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc3/")
EVENS_FOLDER = Path(DATA_FOLDER, "./evens/")
ROOTS_FOLDER = Path(DATA_FOLDER, "./rootBatches/")
ROOTS_BY_SIGMA_FOLDER = Path(DATA_FOLDER, "./rootsBySigma/")

MAX_M = 6
MAX_N = 6

DELTA_N = 1
DELTA_M = 1

def main():
	#previous mxn completed
	m, n = util.load(DATA_FOLDER / "mXn.dat")
	prefixes = util.load(DATA_FOLDER / "prefixes.dat")
	startM = m
	startN = n

	firstST = time.time()
	#m and n are prev m and n expanded to
	while m < MAX_M or n < MAX_N:
		#dM and dN are how much to expand m and n by respectively
		dM = min(DELTA_M, MAX_M - m)
		dN = min(DELTA_N, MAX_N - n)

		print(f"\nExpanding from {m}X{n} to {m+dM}X{n+dN}")

		sT = time.time()

		#expand sideways by dM
		expand.expandSide(DATA_FOLDER, m, n, dM, dN, prefixes)
		sideTime = time.time()
		print(f"Side time: {sideTime - sT}s")
		util.emptyDir(DATA_FOLDER / "parents")
		util.emptyDir(DATA_FOLDER / "oldRoots")

		#expand down by dN
		expand.expandDown(DATA_FOLDER, m, n, dM, dN, prefixes)
		print(f"Down time: {time.time() - sideTime}s")

		endT = time.time()

		m += dM
		n += dN

		#load all evens just for us to check if it's working properly
		# print("genning all evens")
		allEvens = set()
		for x in range(1,n+1):
			eX = util.load(EVENS_FOLDER / f"evens{x}.dat")
			allEvens.update(eX)

		print(f"{m}X{n} total evens: {len(allEvens)}\t in {str(endT-sT)}s")
		print(str(m)+"X"+str(n)+" evens: " + str(allEvens))
		# print(f"size of all evens: {sys.getsizeof(allEvens)}")
		# print(f"Deep allEvens objSize: {get_deep_size(allEvens)}")
		# print()

		#store the m and n completed, evens are stored in side and down expand
		util.store((m,n), DATA_FOLDER / "mXn.dat")
		util.store(prefixes, DATA_FOLDER / "prefixes.dat")

	print(f"\n\nTotal run time for {startM}X{startN} to {m}X{n}: {time.time() - firstST}s ")

#seed the 1x1 board
def seed():
	#make sure all folders exist
	try:
		util.emptyDir(DATA_FOLDER)
	except:
		pass
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
	# util.store(set(), DATA_FOLDER / "roots/rootsBatch0.dat")
	util.store(set([(1,)]), EVENS_FOLDER / "evens1.dat")
	prefixes = set()
	util.store(prefixes, DATA_FOLDER / "prefixes.dat")

if __name__ == '__main__':
	seed()
	main()
