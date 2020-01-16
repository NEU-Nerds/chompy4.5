import util
import os
from pathlib import Path
import time
import expand
import sys
# from settings import *
import settings

# from objsize import get_deep_size

def main():
	#previous mxn completed
	m, n = util.load(settings.DATA_FOLDER / "mXn.dat")
	settings.prefixes = util.load(settings.DATA_FOLDER / "prefixes.dat")
	startM = m
	startN = n

	firstST = time.time()
	#m and n are prev m and n expanded to
	while m < settings.MAX_M or n < settings.MAX_N:
		#dM and dN are how much to expand m and n by respectively
		dM = min(settings.DELTA_M, settings.MAX_M - m)
		dN = min(settings.DELTA_N, settings.MAX_N - n)

		print(f"\nExpanding from {m}X{n} to {m+dM}X{n+dN}")

		sT = time.time()

		#expand sideways by dM
		expand.expandSide(m, n, dM, dN)
		sideTime = time.time()
		print(f"Side time: {sideTime - sT}s")
		util.emptyDir(settings.DATA_FOLDER / "parents")
		util.emptyDir(settings.DATA_FOLDER / "oldRoots")

		#expand down by dN
		expand.expandDown(m, n, dM, dN)
		print(f"Down time: {time.time() - sideTime}s")

		endT = time.time()

		m += dM
		n += dN

		#load all evens just for us to check if it's working properly
		# print("genning all evens")
		allEvens = set()
		for x in range(1,n+1):
			eX = util.load(settings.EVENS_FOLDER / f"evens{x}.dat")
			allEvens.update(eX)

		print(f"{m}X{n} total evens: {len(allEvens)}\t in {str(endT-sT)}s")
		if settings.printEvens:
			print(str(m)+"X"+str(n)+" evens: " + str(allEvens))
		# print(f"size of all evens: {sys.getsizeof(allEvens)}")
		# print(f"Deep allEvens objSize: {get_deep_size(allEvens)}")
		# print()

		#store the m and n completed, evens are stored in side and down expand
		util.store((m,n), settings.DATA_FOLDER / "mXn.dat")
		util.store(settings.prefixes, settings.DATA_FOLDER / "prefixes.dat")

	print(f"\n\nTotal run time for {startM}X{startN} to {m}X{n}: {time.time() - firstST}s ")

#seed the 1x1 board
def seed():
	#make sure all folders exist
	try:
		util.emptyDir(settings.DATA_FOLDER)
	except:
		pass
	try:
		os.mkdir(Path(settings.THIS_FOLDER, "./data"))
	except:
		pass
	try:
		os.mkdir(settings.DATA_FOLDER)
	except:
		pass
	try:
		os.mkdir(settings.EVENS_FOLDER)
	except:
		pass
	try:
		os.mkdir(settings.DATA_FOLDER / "roots")
	except:
		pass
	try:
		os.mkdir(settings.DATA_FOLDER / "oldRoots")
	except:
		pass
	try:
		os.mkdir(settings.DATA_FOLDER / "parents")
	except:
		pass
	try:
		os.mkdir(settings.DATA_FOLDER / "sideOldRoots")
	except:
		pass
	try:
		os.mkdir(settings.DATA_FOLDER / "sideRoots")
	except:
		pass

	util.store((1,1), settings.DATA_FOLDER / "mXn.dat")
	# util.store(set(), DATA_FOLDER / "roots/rootsBatch0.dat")
	util.store(set([(1,)]), settings.EVENS_FOLDER / "evens1.dat")
	prefixes = set()
	util.store(prefixes, settings.DATA_FOLDER / "prefixes.dat")

if __name__ == '__main__':
	settings.init()
	print(f"DATA_FOLDER: {settings.DATA_FOLDER}")
	seed()
	main()
