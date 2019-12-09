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

MAX_M = 12
MAX_N = 12

DELTA_N = 100
DELTA_M = 1

def main():

	#load roots
	m, n = util.load(DATA_FOLDER / "mXn.dat")
	roots = util.load(DATA_FOLDER / "roots.dat")
	#load m,n

	while m < MAX_M or n < MAX_N:
		dM = min(DELTA_M, MAX_M - m)
		dN = min(DELTA_N, MAX_N - n)

		sT = time.time()

		#expand sideways by dM
		roots.update(util.expandSide(EVENS_FOLDER, m, n, dM, dN))
		#expand down by dN
		evens, roots = expandDown(roots, m, n, dM, dN)

		endT = time.time()

		m += dM
		n += dN

		print(str(m)+"X"+str(n)+" #new evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
		# print(str(n)+"X"+str(n)+" evens: " + str(evens))

		#store this depth's evens evens
		util.store((m,n), DATA_FOLDER / "mXn.dat")
		util.store(evens, EVENS_FOLDER / "evens"+str(n)+".dat")
		util.store(roots, DATA_FOLDER / "roots.dat")


def seed():
	roots = set()
	evens = set([(1)])

	try:
		os.mkdir(Path(THIS_FOLDER, "./data")
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
