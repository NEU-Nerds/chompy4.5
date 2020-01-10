import util
import os
import sys
from multiprocessing import Pool
# from objsize import get_deep_size
# import psutil
# from guppy import hpy

#The maximum # of roots in one batch, eventually change to be dependent on
#the length of roots so memory use is constant
MAX_ROOTS = 10 ** 8


def expandDown(DATA_FOLDER, m, n, dM, dN, prefixes):
	#d = depth
	for d in range(n+1, n+dN + 1):
		# print(f"\nExpandingDown d = {d}")

		#clean out unneaded data
		util.emptyDir(DATA_FOLDER / "parents")
		util.emptyDir(DATA_FOLDER / "oldRoots")

		#the good old switheroo (changes roots dir to oldRoots dir)
		os.rename(DATA_FOLDER / "oldRoots", DATA_FOLDER / "rootsTEMP")
		os.rename(DATA_FOLDER / "roots", DATA_FOLDER / "oldRoots")
		os.rename(DATA_FOLDER / "rootsTEMP", DATA_FOLDER / "roots")

		evens = set()
		#oldPrefixes is static
		oldPrefixes = prefixes.copy()

		#load each root batch
		# files = os.listdir(DATA_FOLDER / "oldRoots")
		#will this still work with dynamic prefixes? I think so
		# files.sort()
		ps = list(prefixes)
		ps.sort()
		for f in ps:
			# print(f"file: {f}")
			try:
				roots = util.load(DATA_FOLDER / f"oldRoots/{f}.dat")
			except FileNotFoundError:
				# print(f"couldn't find {f}.dat")
				continue
			prefix = util.getPrefix(list(roots)[0], oldPrefixes)

			#{tuple(prefix):set(roots)}
			newRoots = {}

			#RBS is the roots of the new nodes indexed by the sigma of the node
			#Note a root = node[:-1] (I love how this looks like a face btw)
			rootsBySigma = util.genRBS(roots)
			# print(f"preRBS: {rootsBySigma}")
			#try loading previosu parents
			util.combineDir(DATA_FOLDER / "parents", str(f))
			try:
				prevParents = util.load(DATA_FOLDER / f"parents/{prefix}.dat")
				# print(f"prevParents: {prevParents}")
				for parent in prevParents:
					pRoot = parent[:-1]
					try:
						rootsBySigma[sum(parent)].remove(pRoot)
						util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
					except:
						pass
			except OSError as e:
				# print(f"OSError: {e}")
				pass

			# print(f"postRBS: {rootsBySigma}")

			keys = rootsBySigma.keys()

			#get min and max sigma of nodes in this batch
			minSigma = min(keys)
			maxSigma = max(keys)

			#go through each sigma starting from smallest
			for sigma in range(minSigma, maxSigma + 1):
				#if this sigma is empty why bother
				if sigma not in keys:
					continue
				# print(f"sigma: {sigma}")

				newParents = {}

				#each node here will be even
				for root in rootsBySigma[sigma]:
					#create the node, add it to evens
					node = tuple(list(root) + [sigma - sum(root)] )
					evens.add(node)
					# print(f"node: {node}")
					#get the parents of node
					start = root[0]
					parents = util.getParents(2, m+dM-2, node)
					# print(f"parents: {parents}")

					#create the parent nodes, remove their root from rootsBySigma, add to newRoots
					for parent in parents:
						#if greater than maxSigma then don't bother (won't be in this batch)
						if sum(parent) <= maxSigma:
							pRoot = parent[:-1]
							try:
								rootsBySigma[sum(parent)].remove(pRoot)
								util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
							except:
								pass

						#add parent to be stored dict
						util.addToSet(parent, newParents, oldPrefixes)
				# print(f"newParents: {newParents}")
				#try to load any parents of this sigma already on disk and combine with this batches
				for p in newParents.keys():
					# try:
					# 	oldParents = util.load(DATA_FOLDER / f"parents/{str(p)}.dat")
					# 	oldParents.update(newParents[p])
					# 	combParents = oldParents
					# 	del oldParents
					#
					# except OSError:
					# 	combParents = set(newParents[p])
					#
					# util.store(combParents, DATA_FOLDER / f"parents/{str(p)}.dat")

					util.dirStore(newParents[p], DATA_FOLDER / "parents", str(p))

				newParents.clear()

				for p in newRoots.keys():
					# print(newRoots.keys())
					# print(newRoots[p])
					# print(f"in p: {p}")
					try:
						oldRoots = util.load(DATA_FOLDER / f"roots/{str(p)}.dat")
						oldRoots.update(newRoots[p])
						combRoots = oldRoots
						del oldRoots

					except OSError:
						combRoots = newRoots[p]

					util.store(combRoots, DATA_FOLDER / f"roots/{str(p)}.dat")
					# util.dirStore(newRoots[p], DATA_FOLDER / "roots", str(p))

				newRoots.clear()
				del newParents
				del rootsBySigma[sigma]

			del rootsBySigma


		# for p in oldPrefixes:
		# 	util.combineDir(DATA_FOLDER / "parents", str(p))



			# xs = []
			# for p in oldPrefixes:
			# 	xs.append((DATA_FOLDER / "parents", str(p)))
			# pool = Pool(processes=1)
			# pool.map(util.multiCombineWrapper, xs)


		util.store(evens, DATA_FOLDER / f"evens/evens{d}.dat")
		util.store(prefixes, DATA_FOLDER / "prefixes.dat")
		del evens
	# print("finished all down expands")

def expandSide (DATA_FOLDER, m, n, dM, dN, prefixes):
	# print("\nExpanding Side")

	#initialize the root roots with path len 1
	util.emptyDir(DATA_FOLDER / "sideRoots")
	for x in range(m+1, m+dM + 1):
		# print("storing " + str(x))
		util.store(set([(x,)]), DATA_FOLDER / f"sideRoots/{(x,)}.dat")
		prefixes.add((x,))


	util.store(prefixes, DATA_FOLDER / "prefixes.dat")

	for d in range(2, n + dN):
		expandSideLayer(DATA_FOLDER, d, m, dM, prefixes)

	#take resulting side roots and add them to main roots
	files = os.listdir(DATA_FOLDER / "sideRoots")
	for f in files:
		try:
			oldRoots = util.load(DATA_FOLDER / f"roots/{f}")
			newRoots = util.load(DATA_FOLDER / f"sideRoots/{f}")
			oldRoots.update(newRoots)
			combRoots = oldRoots

			util.store(combRoots, DATA_FOLDER / f"roots/{f}")
		except OSError:

			os.rename(DATA_FOLDER / f"sideRoots/{f}" , DATA_FOLDER / f"roots/{f}")
	# print("finished expandSide")

def expandSideLayer(DATA_FOLDER, depth, pM, dM, prefixes):
	# print("ExpandingSideLayer d = " +str(depth))

	#clean out unneaded data
	util.emptyDir(DATA_FOLDER / "parents")
	util.emptyDir(DATA_FOLDER / "sideOldRoots")

	#the good old switheroo (changes sideRoots dir to sideOldRoots dir)
	os.rename(DATA_FOLDER / "sideOldRoots", DATA_FOLDER / "sideRootsTEMP")
	os.rename(DATA_FOLDER / "sideRoots", DATA_FOLDER / "sideOldRoots")
	os.rename(DATA_FOLDER / "sideRootsTEMP", DATA_FOLDER / "sideRoots")

	#get the parents of the existing evens and store them in parents directory
	#(maybe we should keep this data around - would be a lot faster maybe?)
	evens = util.load(DATA_FOLDER / f"evens/evens{depth}.dat")

	#oldPrefixes is static
	oldPrefixes = prefixes.copy()
	# print(f"evens: {evens}")
	util.genParentsFromExistingEvens(DATA_FOLDER, evens, depth, pM, dM, oldPrefixes)


	#Yes the code below is nearly the same from expand down except the file paths
	#I'll turn it into a function later - Ty. Well we'll see if I do

	#load each root batch
	# files = os.listdir(DATA_FOLDER / "sideOldRoots")
	# files.sort()
	# print(files)
	ps = list(prefixes)
	ps.sort()
	for f in ps:
		# print(f"file: {f}")
		newRoots = {}
		try:
			roots = util.load(DATA_FOLDER / f"sideOldRoots/{f}.dat")
		except:
			continue

		if len(roots) == 0:
			continue

		#RBS is the roots of the new nodes indexed by the sigma of the node
		#Note a root = node[:-1] (I love how this looks like a face btw)
		rootsBySigma = util.genRBS(roots)

		n1 = list(roots)[0]
		prefix = util.getPrefix(n1, oldPrefixes)

		util.combineDir(DATA_FOLDER / "parents", str(f))
		#try loading previosu parents and
		try:
			prevParents = util.load(DATA_FOLDER / f"parents/{prefix}.dat")
			for parent in prevParents:
				pRoot = parent[:-1]
				try:
					rootsBySigma[sum(parent)].remove(pRoot)
					util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
				except:
					pass

		except OSError:
			pass

		keys = rootsBySigma.keys()

		#get min and max sigma
		minSigma = min(keys)
		maxSigma = max(keys)

		#go through each sigma starting from smallest
		for sigma in range(minSigma, maxSigma + 1):
			#if this sigma is empty why bother
			if sigma not in keys:
				continue

			newParents = {}
			allParents = set()

			#each node here will be even
			for root in rootsBySigma[sigma]:
				#create the node, add it to evens
				node = tuple(list(root) + [sigma - sum(root)] )
				evens.add(node)
				# print(f"node: {node}")
				#get the parents of node
				parents = util.getParents(2, pM + dM-2, node)
				# print(f"parents: {parents}")

				#create the parent nodes, remove their root from rootsBySigma, add to newRoots
				for parent in parents:
					#if greater than maxSigma then don't bother (won't be in this batch)
					if sum(parent) <= maxSigma:
						pRoot = parent[:-1]
						try:
							rootsBySigma[sum(parent)].remove(pRoot)
							util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
						except KeyError:
							pass

					#add parent to be stored dict
					# if parent not in allParents:
					util.addToSet(parent, newParents, oldPrefixes)
						# allParents.add(parent)

			#try to load any parents of this sigma already on disk and combine with this batches
			for p in newParents.keys():
				# try:
				# 	oldParents = util.load(DATA_FOLDER / f"parents/{str(p)}.dat")
				# 	if oldParents and newParents[p].issubset(oldParents):
				# 		continue
				# 	oldParents.update(newParents[p])
				# 	combParents = oldParents
				#
				# except OSError:
				# 	combParents = newParents[p]
				#
				# util.store(combParents, DATA_FOLDER / f"parents/{str(p)}.dat")
				util.dirStore(newParents[p], DATA_FOLDER / "parents", str(p))

			newParents.clear()

			for p in newRoots.keys():
				try:
					oldRoots = util.load(DATA_FOLDER / f"sideRoots/{str(p)}.dat")
					if newRoots[p].issubset(oldRoots):
						continue
					oldRoots.update(newRoots[p])
					combRoots = oldRoots

					del oldRoots

				except OSError:
					combRoots = newRoots[p]

				util.store(combRoots, DATA_FOLDER / f"sideRoots/{str(p)}.dat")
			newRoots.clear()
			del newParents
			del rootsBySigma[sigma]

		del rootsBySigma

	util.store(evens, DATA_FOLDER / f"evens/evens{depth}.dat")
	util.store(prefixes, DATA_FOLDER / "prefixes.dat")
	del evens
