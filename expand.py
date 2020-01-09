import util
import os
import sys
# from objsize import get_deep_size
# import psutil
# from guppy import hpy

#The maximum # of roots in one batch, eventually change to be dependent on
#the length of roots so memory use is constant
MAX_ROOTS = 10 ** 6

# MAX_BATCH_DEPTH = 6
# ROOTS_DEPTH = MAX_BATCH_DEPTH - 1
# PARENTS_DEPTH = MAX_BATCH_DEPTH

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
		files = os.listdir(DATA_FOLDER / "oldRoots")
		#will this still work with dynamic prefixes? I think so
		files.sort()
		# print(f"files: {files}")
		for f in files:
			# print(f"\nfile: {f}")
			roots = util.load(DATA_FOLDER / f"oldRoots/{f}")
			# print(f"roots: {roots}")

			n1 = list(roots)[0]
			prefix = util.getPrefix(n1, oldPrefixes)
			# if len(n1) <= ROOTS_DEPTH:
			# 	prefix = 0
			# else:
			# 	prefix = n1[:len(n1)-ROOTS_DEPTH]
			# print(f"prefix: {prefix}")

			#{tuple(prefix):set(roots)}
			newRoots = {}

			#RBS is the roots of the new nodes indexed by the sigma of the node
			#Note a root = node[:-1] (I love how this looks like a face btw)
			rootsBySigma = util.genRBS(roots)

			#try loading previosu parents
			try:
				# print(f"trying to load parents file: {prefix}")
				prevParents = util.load(DATA_FOLDER / f"parents/{prefix}.dat")
				# print(f"prev parents: {prevParents}")
				for parent in prevParents:
					pRoot = parent[:-1]
					try:
						rootsBySigma[sum(parent)].remove(pRoot)
						# print(f"adding {parent} to roots")
						util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
						# print(f"newRoots: {newRoots}")
					except:
						# print("excepted")
						pass

			except OSError as e:
				# print(f"OS error: {e}")
				pass


			# print(f"Size of RBS: {sys.getsizeof(rootsBySigma)}")
			keys = rootsBySigma.keys()

			#get min and max sigma of nodes in this batch
			minSigma = min(keys)
			maxSigma = max(keys)

			#go through each sigma starting from smallest
			for sigma in range(minSigma, maxSigma + 1):
				#if this sigma is empty why bother
				if sigma not in keys:
					continue

				newParents = {}

				#each node here will be even
				# print("going through roots")
				# print(f"RBS {rootsBySigma}")
				for root in rootsBySigma[sigma]:
					#create the node, add it to evens
					node = tuple(list(root) + [sigma - sum(root)] )
					# print(f"node: {node}")
					evens.add(node)

					#get the parents of node
					start = root[0]
					parents = util.getParents(0, m+dM, node)
					# print(f"parents: {parents}")
					#create the parent nodes, remove their root from rootsBySigma, add to newRoots
					for parent in parents:
						#if greater than maxSigma then don't bother (won't be in this batch)
						if sum(parent) <= maxSigma:
							pRoot = parent[:-1]
							try:
								# print(f"removing parent: {parent}\tpRoot: {pRoot}")
								rootsBySigma[sum(parent)].remove(pRoot)
								util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
							except:
								pass

						#add parent to be stored dict
						util.addToSet(parent, newParents, oldPrefixes)

						# if len(parent) <= PARENTS_DEPTH:
						# 	pPrefix = 0
						# else:
						# 	pPrefix = tuple(parent[:len(parent)-PARENTS_DEPTH])
						#
						# if pPrefix in newParents.keys():
						# 	newParents[pPrefix].add(parent)
						# else:
						# 	newParents[pPrefix] = set([parent])

				#try to load any parents of this sigma already on disk and combine with this batches
				# print("STORING")
				for p in newParents.keys():
					# print(f"p: {p}")
					try:
						oldParents = util.load(DATA_FOLDER / f"parents/{str(p)}.dat")
						# print(f"oldParents: {oldParents}\tnewParents: {newParents[p]}")
						oldParents.update(newParents[p])
						combParents = oldParents
						# print("combined")
						del oldParents

					except OSError:
						combParents = set(newParents[p])

					# print(f"down storing parents: {combParents}")
					util.store(combParents, DATA_FOLDER / f"parents/{str(p)}.dat")

				newParents.clear()
				# print(f"newRoots: {newRoots}")
				for p in newRoots.keys():
					# print(f"roots p: {p}")
					try:
						oldRoots = util.load(DATA_FOLDER / f"roots/{str(p)}.dat")
						oldRoots.update(newRoots[p])
						combRoots = oldRoots

						del oldRoots
						# print("combined")

					except OSError:
						combRoots = newRoots[p]
					# print(f"combRoots {combRoots}")
					util.store(combRoots, DATA_FOLDER / f"roots/{str(p)}.dat")
				newRoots.clear()
				# print(f"Deep combParents objSize: {get_deep_size(combParents)}")
				del newParents
				del rootsBySigma[sigma]

			del rootsBySigma

		# print(f"size of newRoots: {sys.getsizeof(newRoots)}")
		# print(f"Deep newRoots objSize: {get_deep_size(newRoots)}")
		# util.store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
		# rootsBatches += 1

		# print("rootsBatches: " + str(rootsBatches))
		# del newRoots
		# print(f"size of evens: {sys.getsizeof(evens)}")
		# print(f"Deep evens objSize: {get_deep_size(evens)}")
		util.store(evens, DATA_FOLDER / f"evens/evens{d}.dat")
		util.store(prefixes, DATA_FOLDER / "prefixes.dat")
		del evens
	# print("finished all down expands")

def expandSide (DATA_FOLDER, m, n, dM, dN, prefixes):
	# print("\nExpanding Side")
	# print(f"m: {m}\tn: {n}\tdM: {dM}\ndN: {dN}")
	#initialize the root roots with path len 1
	roots = set()
	for x in range(m+1, m+dM + 1):
		roots.add((x,))
		prefixes.add((x,))
	# print(f"initRoots: {roots}" )
	util.emptyDir(DATA_FOLDER / "sideRoots")
	util.store(roots, DATA_FOLDER / "sideRoots/0.dat")
	util.store(prefixes, DATA_FOLDER / "prefixes.dat")

	for d in range(2, n + dN):
		# print(f"d: {d}")
		expandSideLayer(DATA_FOLDER, d, m, dM, prefixes)

	#take resulting side roots and add them to main roots
	files = os.listdir(DATA_FOLDER / "sideRoots")
	# print(f"combining files: {files}")
	for f in files:
		try:
			oldRoots = util.load(DATA_FOLDER / f"roots/{f}")
			# print(f"oldRoots: {oldRoots}")
			newRoots = util.load(DATA_FOLDER / f"sideRoots/{f}")
			# print(f"newRoots: {newRoots}")
			oldRoots.update(newRoots)
			combRoots = oldRoots
			# print(f"combRoots: {combRoots}")
			util.store(combRoots, DATA_FOLDER / f"roots/{f}")
		except OSError:
			# print("renaming")
			os.rename(DATA_FOLDER / f"sideRoots/{f}" , DATA_FOLDER / f"roots/{f}")
	# util.store(prefixes, DATA_FOLDER / "prefixes.dat")
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

	util.genParentsFromExistingEvens(DATA_FOLDER, evens, depth, pM, dM, oldPrefixes)


	#Yes the code below is nearly the same from expand down except the file paths
	#I'll turn it into a function later - Ty. Well we'll see if I do

	#load each root batch
	files = os.listdir(DATA_FOLDER / "sideOldRoots")
	files.sort()
	for f in files:
		# print(f"file: {f}")
		newRoots = {}

		roots = util.load(DATA_FOLDER / f"sideOldRoots/{f}")
		if len(roots) == 0:
			continue
		# print(f"roots: {roots}")
		#RBS is the roots of the new nodes indexed by the sigma of the node
		#Note a root = node[:-1] (I love how this looks like a face btw)
		rootsBySigma = util.genRBS(roots)
		# print(f"RBS: {rootsBySigma}")

		n1 = list(roots)[0]
		prefix = util.getPrefix(n1, oldPrefixes)
		# if len(n1) <= PARENTS_DEPTH:
		# 	prefix = 0
		# else:
		# 	prefix = n1[:len(n1)-PARENTS_DEPTH]
		# print(f"prefix: {prefix}")

		#try loading previosu parents and
		try:
			# print("trying to load parents")
			prevParents = util.load(DATA_FOLDER / f"parents/{prefix}.dat")
			# print(f"loaded prevParents: {prevParents}")
			# print(f"Deep prevParents objSize: {get_deep_size(prevParents)}")
			for parent in prevParents:
				# print(f"parent: {parent}")
				pRoot = parent[:-1]
				try:

					rootsBySigma[sum(parent)].remove(pRoot)
					# print(f"adding parent from existing: {parent}")
					util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
					# print(f"newRoots: {newRoots}")
				except Exception as e:
					# print(f"excpetion {e}")
					pass

		except OSError as e:
			# print(f"osError: {e}")
			pass
		# print(f"Size of RBS: {sys.getsizeof(rootsBySigma)}")
		keys = rootsBySigma.keys()

		#get min and max sigma
		minSigma = min(keys)
		maxSigma = max(keys)

		#go through each sigma starting from smallest
		for sigma in range(minSigma, maxSigma + 1):
			# print(f"sigma: {sigma}")
			#if this sigma is empty why bother
			if sigma not in keys:
				continue

			newParents = {}
			allParents = set()

			#each node here will be even
			for root in rootsBySigma[sigma]:
				# print(f"root: {root}")
				#create the node, add it to evens
				node = tuple(list(root) + [sigma - sum(root)] )
				# print(f"node: {node}")
				evens.add(node)

				#get the parents of node
				start = root[0]
				# print(f"node: {node}\t start: {start}\t pM: {pM}")
				parents = util.getParents(0, pM + dM, node)
				# print(f"parents: {parents}")
				#create the parent nodes, remove their root from rootsBySigma, add to newRoots
				for parent in parents:
					# print(f"Parent: {parent}")
					#if greater than maxSigma then don't bother (won't be in this batch)
					if sum(parent) <= maxSigma:
						pRoot = parent[:-1]
						try:
							# print(f"preRBS: {rootsBySigma}")
							rootsBySigma[sum(parent)].remove(pRoot)
							# print(f"postRBS: {rootsBySigma}")
							# print(f"adding parent from new: {parent}")
							util.addToSet(parent, newRoots, prefixes, MAX_ROOTS)
							# print(f"newRoots2: {newRoots}")
						except KeyError:
							pass

					#add parent to be stored dict
					# if parent not in allParents:
					util.addToSet(parent, newParents, oldPrefixes)
						# allParents.add(parent)

					# if len(parent) <= PARENTS_DEPTH:
					# 	pPrefix = 0
					# else:
					# 	pPrefix = tuple(parent[:len(parent)-PARENTS_DEPTH])
					#
					# if pPrefix in newParents.keys():
					# 	newParents[pPrefix].add(parent)
					# else:
					# 	newParents[pPrefix] = set([parent])

			#try to load any parents of this sigma already on disk and combine with this batches
			# print(f"newParents: {newParents}")
			# print("\nNEW STORE")
			for p in newParents.keys():
				# if p == 0:
				# 	newP = 0
				# else:
				# 	newP = p[:-1]
				# print(f"Storing p: {p}\tparents: {newParents[p]}")
				try:
					oldParents = util.load(DATA_FOLDER / f"parents/{str(p)}.dat")
					if oldParents and newParents[p].issubset(oldParents):
						continue
					oldParents.update(newParents[p])
					combParents = oldParents
					# print("combined")
				except OSError as e:
					# print(f"error: {e}")
					combParents = newParents[p]
				# print(f"p: {p}")
				# print(f"side storing parents: {combParents}")
				util.store(combParents, DATA_FOLDER / f"parents/{str(p)}.dat")

			newParents.clear()

			# print("\nNEW STORE")
			for p in newRoots.keys():
				# print(f"Storing p: {p}\tnewRoots[p]: {newRoots[p]}")
				try:
					oldRoots = util.load(DATA_FOLDER / f"sideRoots/{str(p)}.dat")
					# print(f"odlRoots: {oldRoots}")
					if newRoots[p].issubset(oldRoots):
						continue
					oldRoots.update(newRoots[p])
					combRoots = oldRoots

					del oldRoots

				except OSError:
					combRoots = newRoots[p]

				# print(f"combRoots {combRoots}")
				util.store(combRoots, DATA_FOLDER / f"sideRoots/{str(p)}.dat")
			newRoots.clear()
			# del storeParents
			# del combParents
			del newParents
			del rootsBySigma[sigma]

		del rootsBySigma

	# del newRoots
	# print(f"size of evens: {sys.getsizeof(evens)}")
	util.store(evens, DATA_FOLDER / f"evens/evens{depth}.dat")
	util.store(prefixes, DATA_FOLDER / "prefixes.dat")
	del evens
