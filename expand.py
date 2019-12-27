import util
import os

#The maximum # of roots in one batch, eventually change to be dependent on
#the length of roots so memory use is constant
MAX_ROOTS = 10 ** 6

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
		newRoots = set()
		#the number of rootsBatches stored to disk already
		rootsBatches = 0

		#load each root batch
		numRootBatches = len(os.listdir(DATA_FOLDER / "oldRoots"))
		for i in range(numRootBatches):
			roots = util.load(DATA_FOLDER / f"oldRoots/rootsBatch{i}.dat")

			#RBS is the roots of the new nodes indexed by the sigma of the node
			#Note a root = node[:-1] (I love how this looks like a face btw)
			rootsBySigma = util.genRBS(roots)
			keys = rootsBySigma.keys()

			#get min and max sigma of nodes in this batch
			minSigma = min(keys)
			maxSigma = max(keys)

			#go through each sigma starting from smallest
			for sigma in range(minSigma, maxSigma + 1):
				#new parents to be stored to disk for future batches
				storeParents = set()

				#if this sigma is empty why bother
				if sigma not in keys:
					continue

				#try loading previous parents with this sigma from disk and
				#remove those nodes' roots from RBS
				try:
					prevParents = util.load(DATA_FOLDER / f"parents/parentsSigma{sigma}.dat")
					for parent in prevParents:
						pRoot = parent[:-1]
						try:
							rootsBySigma[sum(parent)].remove(pRoot)
							newRoots.add(parent)
						except:
							pass

						if len(newRoots) >= MAX_ROOTS:
							util.store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
							rootsBatches += 1
							newRoots.clear()

				except OSError:
					prevParents = None

				#each node here will be even
				for root in rootsBySigma[sigma]:
					#create the node, add it to evens
					node = tuple(list(root) + [sigma - sum(root)] )
					evens.add(node)

					#get the parents of node
					start = root[0]
					parents = util.getParents(start, (m)-start, node)

					#create the parent nodes, remove their root from rootsBySigma, add to newRoots
					for parent in parents:
						#if greater than maxSigma then don't bother (won't be in this batch)
						if sum(parent) <= maxSigma:
							pRoot = parent[:-1]
							try:
								rootsBySigma[sum(parent)].remove(pRoot)
								newRoots.add(parent)
							except:
								pass

							#check if newRoots needs to be dumped to disk
							if len(newRoots) >= MAX_ROOTS:
								util.store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
								rootsBatches += 1
								newRoots.clear()

						#add parent to be stored list
						storeParents.add(parent)

				#try to load any parents of this sigma already on disk and combine with this batches
				if prevParents:
					combParents = prevParents.union(storeParents)
					del prevParents
				else:
					combParents = storeParents

				util.store(combParents, DATA_FOLDER / f"parents/parentsSigma{sigma}.dat")

				del storeParents
				del combParents
				del rootsBySigma[sigma]

			del rootsBySigma

		util.store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
		rootsBatches += 1

		# print("rootsBatches: " + str(rootsBatches))
		del newRoots
		util.store(evens, DATA_FOLDER / f"evens/evens{d}.dat")
		del evens
	# print("finished all down expands")

def expandSide (DATA_FOLDER, m, n, dM, dN):
	# print("\nExpanding Side")

	#initialize the root roots with path len 1
	roots = set()
	for x in range(m+1, m+dM + 1):
		roots.add((x,))
	util.emptyDir(DATA_FOLDER / "sideRoots")
	util.store(roots, DATA_FOLDER / "sideRoots/rootsBatch0.dat")

	for d in range(2, n + dN):
		# print(f"d: {d}")

		expandSideLayer(DATA_FOLDER, d, m, dM)

	#take resulting side roots and add them to main roots
	#currently not combining batches cause that would be more work but maybe worth it??
	numRootBatches = len(os.listdir(DATA_FOLDER / "roots"))
	for i in range(len(os.listdir(DATA_FOLDER / "sideRoots"))):
		os.rename(DATA_FOLDER / f"sideRoots/rootsBatch{i}.dat", DATA_FOLDER / f"roots/rootsBatch{numRootBatches+i}.dat")
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
	util.genParentsFromExistingEvens(DATA_FOLDER, evens, depth, pM, dM)

	#new roots is dumped to disk when it hits MAX_ROOTS and cleared
	newRoots = set()
	#the number of rootsBatches stored to disk already
	rootsBatches = 0

	#Yes the code below is nearly the same from expand down except the file paths
	#I'll turn it into a function later - Ty

	#load each root batch
	numRootBatches = len(os.listdir(DATA_FOLDER / "sideOldRoots"))
	for i in range(numRootBatches):
		roots = util.load(DATA_FOLDER / f"sideOldRoots/rootsBatch{i}.dat")

		#RBS is the roots of the new nodes indexed by the sigma of the node
		#Note a root = node[:-1] (I love how this looks like a face btw)
		rootsBySigma = util.genRBS(roots)
		keys = rootsBySigma.keys()

		#get min and max sigma
		minSigma = min(keys)
		maxSigma = max(keys)

		#go through each sigma starting from smallest
		for sigma in range(minSigma, maxSigma + 1):
			#new parents to be stored to disk for future batches
			storeParents = set()

			#if this sigma is empty why bother
			if sigma not in keys:
				continue

			#try loading previous parents with this sigma from disk and
			#remove those nodes' roots from RBS
			try:
				prevParents = util.load(DATA_FOLDER / f"parents/parentsSigma{sigma}.dat")
				for parent in prevParents:
					pRoot = parent[:-1]
					try:
						rootsBySigma[sum(parent)].remove(pRoot)
						newRoots.add(parent)
					except:
						pass

					if len(newRoots) >= MAX_ROOTS:
						util.store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
						rootsBatches += 1
						newRoots.clear()

			except OSError:
				prevParents = None

			#each node here will be even
			for root in rootsBySigma[sigma]:
				#create the node, add it to evens
				node = tuple(list(root) + [sigma - sum(root)] )
				evens.add(node)

				#get the parents of node
				start = root[0]
				parents = util.getParents(start, (pM)-start, node)

				#create the parent nodes, remove their root from rootsBySigma, add to newRoots
				for parent in parents:
					#if greater than maxSigma then don't bother (won't be in this batch)
					if sum(parent) <= maxSigma:
						pRoot = parent[:-1]
						try:
							rootsBySigma[sum(parent)].remove(pRoot)
							newRoots.add(parent)
						except:
							pass

						#check if newRoots needs to be dumped to disk
						if len(newRoots) >= MAX_ROOTS:
							# print("STORING NEW ROOTS")
							util.store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
							rootsBatches += 1
							newRoots.clear()

					#add to be stored list
					storeParents.add(parent)

			#try to load any parents of this sigma already on disk and combine with this batches
			if prevParents:
				combParents = prevParents.union(storeParents)
				del prevParents
			else:
				combParents = storeParents

			util.store(combParents, DATA_FOLDER / f"parents/parentsSigma{sigma}.dat")

			del storeParents
			del combParents
			del rootsBySigma[sigma]

		del rootsBySigma

	util.store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
	rootsBatches += 1

	# print("rootsBatches: " + str(rootsBatches))
	del newRoots
	util.store(evens, DATA_FOLDER / f"evens/evens{depth}.dat")
	del evens
