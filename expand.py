import util
import os
import sys
# from objsize import get_deep_size
# import psutil
# from guppy import hpy

#The maximum # of roots in one batch, eventually change to be dependent on
#the length of roots so memory use is constant
MAX_ROOTS = 10 ** 6

MAX_BATCH_DEPTH = 7

def expandDown(DATA_FOLDER, m, n, dM, dN):
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
		#new roots is dumped to disk when it hits MAX_ROOTS and cleared
		# newRoots = set()


		#load each root batch
		# numRootBatches = len(os.listdir(DATA_FOLDER / "oldRoots"))
		files = os.listdir(DATA_FOLDER / "oldRoots")
		files.sort()
		# print(f"files: {files}")
		for f in files:
			#get the prefix for this batch
			# prefix = []
			# c = 0
			# while c < len(f) and f[c] != ".":
			# 	prevC = c
			# 	while c < len(f) and f[c] != "." and f[c] != "-":
			# 		c += 1
			# 	prefix.append(int(f[prevC:c]))
			# 	if f[c] == ".":
			# 		break
			# 	else:
			# 		c += 1


			#{tuple(prefix):set(roots)}
			newRoots = {}
			roots = util.load(DATA_FOLDER / f"oldRoots/{f}")
			# print(f"size of roots: {sys.getsizeof(roots)}")
			# print(f"Deep roots objSize: {get_deep_size(roots)}")
			#RBS is the roots of the new nodes indexed by the sigma of the node
			#Note a root = node[:-1] (I love how this looks like a face btw)
			# print(f"roots: {roots}")
			rootsBySigma = util.genRBS(roots, True)

			#try loading previosu parents and
			try:
				prevParents = util.load(DATA_FOLDER / f"parents/{f}")
				# print(f"Deep prevParents objSize: {get_deep_size(prevParents)}")
				for parent in prevParents:
					pRoot = parent[:-1]
					try:
						rootsBySigma[sum(parent)].remove(pRoot)
						util.addToNewRoots(parent, newRoots, MAX_BATCH_DEPTH)
						# newRoots.add(parent)
					except:
						pass

					# if len(newRoots) >= MAX_ROOTS:
					# 	# print(f"size of newRoots: {sys.getsizeof(newRoots)}")
					# 	# print(f"Deep newRoots objSize: {get_deep_size(newRoots)}")
					# 	# print(f"size of evens: {sys.getsizeof(evens)}")
					# 	# print(f"Deep evens objSize: {get_deep_size(evens)}")
					# 	util.store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
					# 	rootsBatches += 1
					# 	newRoots.clear()

			except OSError:
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

				# print(f"Sigma {sigma}")
				# process = psutil.Process(os.getpid())
				# if int(process.memory_info().rss) > 7 * (10**9):
				# 	h = hpy()
				# 	print(h.heap())
					# exit()
				# print("past heap")

				#new parents to be stored to disk for future batches
				# storeParents = set()

				#try loading previous parents with this sigma from disk and
				#remove those nodes' roots from RBS

				#each node here will be even
				# print("going through roots")
				for root in rootsBySigma[sigma]:
					#create the node, add it to evens
					node = tuple(list(root) + [sigma - sum(root)] )
					# print(f"node: {node}")
					evens.add(node)

					#get the parents of node
					start = root[0]
					# parents = util.getParents(start, (m)-start, node)
					parents = util.getParents(0, m+dM, node)
					# print(f"parents: {parents}")
					#create the parent nodes, remove their root from rootsBySigma, add to newRoots
					for parent in parents:
						#if greater than maxSigma then don't bother (won't be in this batch)
						if sum(parent) <= maxSigma:
							pRoot = parent[:-1]
							try:
								rootsBySigma[sum(parent)].remove(pRoot)
								# newRoots.add(parent)
								util.addToNewRoots(parent, newRoots, MAX_BATCH_DEPTH)
							except:
								pass

							# #check if newRoots needs to be dumped to disk
							# if len(newRoots) >= MAX_ROOTS:
							# 	# print(f"size of newRoots: {sys.getsizeof(newRoots)}")
							# 	# print(f"Deep newRoots objSize: {get_deep_size(newRoots)}")
							# 	# print(f"size of evens: {sys.getsizeof(evens)}")
							# 	# print(f"Deep evens objSize: {get_deep_size(evens)}")
							# 	util.store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
							# 	rootsBatches += 1
							# 	newRoots.clear()

						#add parent to be stored dict
						if len(parent) > MAX_BATCH_DEPTH:
							pPrefix = tuple(parent[:len(parent)-MAX_BATCH_DEPTH])
						else:
							pPrefix = 0
						if pPrefix in newParents.keys():
							newParents[pPrefix].add(parent)
						else:
							newParents[pPrefix] = set(parent)

				#try to load any parents of this sigma already on disk and combine with this batches
				for p in newParents.keys():
					try:
						oldParents = util.load(DATA_FOLDER / f"parents/{str(p)}.dat")
						combParents = oldParents.union(newParents[p])
						del oldParents

					except OSError:
						combParents = newParents[p]
					# print(f"p: {p}")
					util.store(combParents, DATA_FOLDER / f"parents/{str(p)}.dat")

				for p in newRoots.keys():
					try:
						oldRoots = util.load(DATA_FOLDER / f"roots/{str(p)}.dat")
						combRoots = oldRoots.union(newRoots[p])
						del oldRoots

					except OSError:
						combRoots = newRoots[p]
					# print(f"combRoots {combRoots}")
					util.store(combRoots, DATA_FOLDER / f"roots/{str(p)}.dat")

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
		del evens
	# print("finished all down expands")

def expandSide (DATA_FOLDER, m, n, dM, dN):
	print("\nExpanding Side")
	# print(f"m: {m}\tn: {n}\tdM: {dM}\ndN: {dN}")
	#initialize the root roots with path len 1
	roots = set()
	for x in range(m+1, m+dM + 1):
		roots.add((x,))
	# print(f"initRoots: {roots}" )
	util.emptyDir(DATA_FOLDER / "sideRoots")
	util.store(roots, DATA_FOLDER / "sideRoots/0.dat")

	for d in range(2, n + dN):
		# print(f"d: {d}")

		expandSideLayer(DATA_FOLDER, d, m, dM)

	#take resulting side roots and add them to main roots
	#currently not combining batches cause that would be more work but maybe worth it??
	# numRootBatches = len(os.listdir(DATA_FOLDER / "roots"))
	# for i in range(len(os.listdir(DATA_FOLDER / "sideRoots"))):
	# 	os.rename(DATA_FOLDER / f"sideRoots/rootsBatch{i}.dat", DATA_FOLDER / f"roots/rootsBatch{numRootBatches+i}.dat")

	files = os.listdir(DATA_FOLDER / "sideRoots")
	# print(f"files: {files}")
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



	# print("finished expandSide")

def expandSideLayer(DATA_FOLDER, depth, pM, dM):
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
	util.genParentsFromExistingEvens(DATA_FOLDER, evens, depth, pM, dM, MAX_BATCH_DEPTH)


	#Yes the code below is nearly the same from expand down except the file paths
	#I'll turn it into a function later - Ty

	#load each root batch
	files = os.listdir(DATA_FOLDER / "sideOldRoots")
	files.sort()

	for f in files:
		# print(f"f: {f}")
		newRoots = {}

		roots = util.load(DATA_FOLDER / f"sideOldRoots/{f}")

		#RBS is the roots of the new nodes indexed by the sigma of the node
		#Note a root = node[:-1] (I love how this looks like a face btw)
		rootsBySigma = util.genRBS(roots)

		#try loading previosu parents and
		try:
			prevParents = util.load(DATA_FOLDER / f"parents/{f}")
			# print(f"loaded prevParents: {prevParents}")
			# print(f"Deep prevParents objSize: {get_deep_size(prevParents)}")
			for parent in prevParents:

				pRoot = parent[:-1]
				try:

					rootsBySigma[sum(parent)].remove(pRoot)
					# print(f"adding parent from existing: {parent}")
					util.addToNewRoots(parent, newRoots, MAX_BATCH_DEPTH)
					# print(f"newRoots: {newRoots}")
					# newRoots.add(parent)
				except Exception as e:
					# print(f"excpetion {e}")
					pass

		except OSError as e:
			# print(f"osError: {e}")
			# print(os.listdir(DATA_FOLDER / "parents"))
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

			#try loading previous parents with this sigma from disk and
			#remove those nodes' roots from RBS
			# try:
			# 	prevParents = util.load(DATA_FOLDER / f"parents/parentsSigma{sigma}.dat")
			# 	for parent in prevParents:
			# 		pRoot = parent[:-1]
			# 		try:
			# 			rootsBySigma[sum(parent)].remove(pRoot)
			# 			newRoots.add(parent)
			# 		except:
			# 			pass
			#
			# 		if len(newRoots) >= MAX_ROOTS:
			# 			# print(f"size of newRoots: {sys.getsizeof(newRoots)}")
			# 			util.store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
			# 			rootsBatches += 1
			# 			newRoots.clear()
			#
			# except OSError:
			# 	prevParents = None

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
				# parents = util.getParents(start, (pM)-start, node)
				parents = util.getParents(pM, dM, node)
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
							util.addToNewRoots(parent, newRoots, MAX_BATCH_DEPTH)
							# print(f"newRoots2: {newRoots}")
						except:
							pass

						# #check if newRoots needs to be dumped to disk
						# if len(newRoots) >= MAX_ROOTS:
						# 	# print("STORING NEW ROOTS")
						# 	# print(f"size of newRoots: {sys.getsizeof(newRoots)}")
						# 	util.store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
						# 	rootsBatches += 1
						# 	newRoots.clear()
					#add parent to be stored dict
					if len(parent) > MAX_BATCH_DEPTH:
						pPrefix = tuple(parent[:len(parent)-MAX_BATCH_DEPTH])
					else:
						pPrefix = 0
					if pPrefix in newParents.keys():
						newParents[pPrefix].add(parent)
					else:
						newParents[pPrefix] = set([parent])
					#add to be stored list
					# storeParents.add(parent)

			#try to load any parents of this sigma already on disk and combine with this batches
			#try to load any parents of this sigma already on disk and combine with this batches
			# print(f"newParents: {newParents}")
			for p in newParents.keys():
				try:
					oldParents = util.load(DATA_FOLDER / f"parents/{str(p)}.dat")
					combParents = oldParents.union(newParents[p])
					del oldParents

				except OSError:
					combParents = newParents[p]
				# print(f"p: {p}")
				util.store(combParents, DATA_FOLDER / f"parents/{str(p)}.dat")

			# print("\nNEW STORE")
			for p in newRoots.keys():
				# print("Storing")
				# print(f"p: {p}")
				# print(f"newRoots[p]: {newRoots[p]}")
				try:
					oldRoots = util.load(DATA_FOLDER / f"sideRoots/{str(p)}.dat")
					# print(f"odlRoots: {oldRoots}")
					combRoots = oldRoots.union(newRoots[p])
					del oldRoots

				except OSError:
					combRoots = newRoots[p]

				# print(f"combRoots {combRoots}")
				util.store(combRoots, DATA_FOLDER / f"sideRoots/{str(p)}.dat")
			# del storeParents
			# del combParents
			del newParents
			del rootsBySigma[sigma]

		del rootsBySigma
	# print(f"size of newRoots: {sys.getsizeof(newRoots)}")
	# util.store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
	# rootsBatches += 1

	# print("rootsBatches: " + str(rootsBatches))
	del newRoots
	# print(f"size of evens: {sys.getsizeof(evens)}")
	util.store(evens, DATA_FOLDER / f"evens/evens{depth}.dat")
	del evens
