import util
import os
import sys
from multiprocessing import Pool
import settings
import shutil
# from objsize import get_deep_size
# import psutil
# from guppy import hpy


def expandSide (m, n, dM, dN):
	# print("\nExpanding Side")
	#?
	settings.staticPrefixes = settings.prefixes.copy()

	settings.currRootsDir = settings.DATA_FOLDER / "sideRoots"
	settings.currOldRootsDir = settings.DATA_FOLDER / "sideOldRoots"
	#initialize the root roots with path len 1
	util.emptyDir(settings.DATA_FOLDER / "sideRoots")
	for x in range(m+1, m+dM + 1):
		util.store(set([(x,)]), settings.DATA_FOLDER / f"sideRoots/{(x,)}.dat")
		settings.prefixes.add((x,))

	util.store(settings.prefixes, settings.DATA_FOLDER / "prefixes.dat")
	newEvens = set()
	for d in range(2, n + dN):
		expandSideLayer(d, m, dM, newEvens)

	#get Conjugates of side evens for down evens
	nextEvens = set()
	for e in newEvens:
		nextEvens.add(util.getConjugate(e))

	#Add the Square even manually
	cornerEven = tuple([m+dM] + [1]* (n+dN-1))
	nextEvens.add(cornerEven)

	#store new evens
	util.store(nextEvens, settings.DATA_FOLDER / f"evens/evens{n+dN}.dat")

	# print("finished expandSide")

def expandSideLayer(depth, m, dM, newEvens = set()):
	# print("ExpandingSideLayer d = " +str(depth))

	#clean out unneaded data
	util.emptyDir(settings.DATA_FOLDER / "parents")
	util.emptyDir(settings.DATA_FOLDER / "sideOldRoots")

	#the good old switheroo (changes sideRoots dir to sideOldRoots dir)
	os.rename(settings.DATA_FOLDER / "sideOldRoots", settings.DATA_FOLDER / "sideRootsTEMP")
	os.rename(settings.DATA_FOLDER / "sideRoots", settings.DATA_FOLDER / "sideOldRoots")
	os.rename(settings.DATA_FOLDER / "sideRootsTEMP", settings.DATA_FOLDER / "sideRoots")

	#get the parents of the existing evens and store them in parents directory
	#(maybe we should keep this data around - would be a lot faster maybe?)
	evens = util.load(settings.DATA_FOLDER / f"evens/evens{depth}.dat")



	# print(f"evens: {evens}")
	settings.staticPrefixes = settings.prefixes.copy()
	util.emptyDir(settings.PARENTS_FOLDER)
	util.genParentsFromExistingEvens(evens, depth, m, dM)

	expandMain(depth, m, dM, True, evens, newEvens)
	#Yes the code below is nearly the same from expand down except the file paths
	#I'll turn it into a function later - Ty. Well we'll see if I do



def expandMain(depth, m, dM, isSide, evens = set(), newEvens = set()):
	# print("expanding main")


	#static
	settings.staticPrefixes = settings.prefixes.copy()
	ps = list(settings.staticPrefixes)
	ps.sort()
	for f in ps:
		# print(f"file: {f}")
		newRoots = {}
		workingParents = set()
		settings.currParentsNum = 0
		util.combineDir(settings.currRootsDir, str(f), True)
		# util.combineDir(settings.PARENTS_FOLDER, str(f), True)
		try:
			roots = util.load(f"{settings.currOldRootsDir}/{f}.dat")
		except Exception as e:
			# print(f"error: {e}")
			continue
		# print(f"roots: {roots}")

		if len(roots) == 0:
			continue


		#RBS is the roots of the new nodes indexed by the sigma of the node
		#Note a root = node[:-1] (I love how this looks like a face btw)
		rootsBySigma = util.genRBS(roots)
		# print(f"RBS: {rootsBySigma}")

		# n1 = list(roots)[0]
		# prefix = util.getPrefix(n1, oldPrefixes)

		# print(os.listdir(settings.PARENTS_FOLDER))
		util.combineDir(settings.PARENTS_FOLDER, str(f))
		# if f == (6, 4):
			# print("NUM FILES: "+str(len(os.listdir(DATA_FOLDER / f"parents/{f}" ))))

		#try loading previosu parents and
		try:
			prevParents = util.load(settings.PARENTS_FOLDER / f"{f}.dat")
			# print(f"prevParents: {prevParents}")
			for parent in prevParents:
				pRoot = parent[:-1]
				try:
					# print("trying")
					rootsBySigma[sum(parent)].remove(pRoot)
					# print("2")
					util.addToSet(parent, newRoots, root=True)
				except Exception as e:
					# print
					# print(f"error rbs: {e}")
					pass


		except OSError as e:
			# print(f"OSerror: {e}")
			pass
			# print(f"error: {e}")


		#go through each sigma starting from smallest
		for sigma in range(min(rootsBySigma.keys()), max(rootsBySigma.keys()) + 1):
			#if this sigma is empty why bother
			# print(f"sigma: {sigma}")
			if sigma not in rootsBySigma.keys():
				continue

			#each node here will be even
			for root in rootsBySigma[sigma]:
				#create the node, add it to evens
				# print("starting")
				node = tuple(list(root) + [sigma - sum(root)] )
				evens.add(node)
				newEvens.add(node)
				# print(f"node: {node}")

				#get the parents of node
				# parents = util.getParents(2, pM + dM-2, node)
				start = node[0]-1
				delta = m+dM - (node[0]-1)
				# parentD = m+dM

				if (isSide):
					start = m
					delta = dM
				# 	parentD = m+dM-node[-1]
				# print(f"pre parents {rootsBySigma}")
				util.getParents(start, delta, node, workingParents, rootsBySigma, newRoots)

			for p in newRoots.keys():
				util.dirStore(newRoots[p], settings.currRootsDir, str(p))

			newRoots.clear()
			# del newParents
			del rootsBySigma[sigma]

		del rootsBySigma
		# print(f"workingParents: {workingParents}")
		util.storeParents(workingParents)

		try:
			shutil.rmtree(settings.PARENTS_FOLDER / str(f))
		except:
			pass
		try:
			os.unlink(settings.PARENTS_FOLDER / f"{f}.dat")
		except:
			pass

	for p in settings.prefixes:
		util.combineDir(settings.currRootsDir, str(p), True)

	util.store(evens, settings.DATA_FOLDER / f"evens/evens{depth}.dat")
	util.store(settings.prefixes, settings.DATA_FOLDER / "prefixes.dat")
	del evens
