import pickle
import os
import shutil

MAX_ROOTS = 10 ** 4

def expandDown(DATA_FOLDER, m, n, dM, dN):
	for d in range(n+1, n+dN + 1):

		emptyDir(DATA_FOLDER / "parents")
		emptyDir(DATA_FOLDER / "oldRoots")

		os.rename(DATA_FOLDER / "oldRoots", DATA_FOLDER / "rootsTEMP")
		os.rename(DATA_FOLDER / "roots", DATA_FOLDER / "oldRoots")
		os.rename(DATA_FOLDER / "rootsTEMP", DATA_FOLDER / "roots")



		evens = set()
		#max = MAX_ROOTS
		newRoots = set()
		rootsBatches = 0

		#load each root batch
		numRootBatches = len(os.listdir(DATA_FOLDER / "oldRoots"))
		for i in range(numRootBatches):
			roots = load(DATA_FOLDER / f"oldRoots/rootsBatch{i}.dat")
			print(f"rootsBatch {i}")
			#created rootsBySigma batch
			rootsBySigma = {}
			keys = set()
			for root in roots:
				# print(f"root: {root}")
				# print(f"preRootsBySigma: {rootsBySigma}")
				for t in range(1, root[-1] + 1):
					# print("t: " +str(t))
					key = sum(root) + t
					# print(f"key: {key}")
					if key in keys:
						# print("key was already there")
						rootsBySigma[key].add(root)
					else:
						# print("key wasn't there")
						rootsBySigma[key] = set([root])
						keys.add(key)
			# print(f"rootsBySigma: {rootsBySigma}")

			#get min and max sigma
			minSigma = min(keys)
			maxSigma = max(keys)



			for sigma in range(minSigma, maxSigma + 1):
				# print(f"Sigma: {sigma}")

				storeParents = set()

				#if this sigma is empty
				if sigma not in keys:
					# print("nothing here")
					continue
				# print(f"preRootsBySigma: {rootsBySigma[sigma]}")
				try:
					prevParents = load(DATA_FOLDER / f"parents/parentsSigma{sigma}.dat")
					# print(f"prevParents exists: {prevParents}")
					for parent in prevParents:
						pRoot = parent[:-1]
						try:
							rootsBySigma[sum(parent)].remove(pRoot)
							newRoots.add(parent)
						except:
							pass

						if len(newRoots) >= MAX_ROOTS:
							# print("STORING NEW ROOTS")
							store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
							rootsBatches += 1
							newRoots.clear()
							# print(f"newRoots post clear: {newRoots}")


				except:
					prevParents = None

				# print(f"postRootsBySigma: {rootsBySigma[sigma]}")

				for root in rootsBySigma[sigma]:
					#create the node, add it to evens
					node = tuple(list(root) + [sigma - sum(root)] )
					# print(f"node: {node}")

					#add maxEvens?
					evens.add(node)

					#get the parents of node
					start = root[0]
					parents = getParents(start, (m)-start, node)
					# print(f"parents: {parents}")

					#create the parent nodes, remove their root from rootsBySigma, add to newRoots
					for parent in parents:
						pSigma = sum(parent)
						# print(f"Node parent: {parent}")
						# print(f"rootsBySigma: {rootsBySigma}")
						#if greater than maxSigma then don't bother
						if pSigma <= maxSigma:
							pRoot = parent[:-1]
							try:
								rootsBySigma[sum(parent)].remove(pRoot)
								newRoots.add(parent)
								# print("added parent to newRoots")
							except:
								pass
							if len(newRoots) >= MAX_ROOTS:
								# print("STORING NEW ROOTS")
								store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
								rootsBatches += 1
								newRoots.clear()



						#add to be stored list
						storeParents.add(parent)
						#ADD MAX PARENTS LATER


				# print(f"newRoots: {newRoots}")
				if prevParents:
					combParents = prevParents.union(storeParents)
					del prevParents
				else:
					combParents = storeParents

				del storeParents

				store(combParents, DATA_FOLDER / f"parents/parentsSigma{sigma}.dat")

				del combParents
				del rootsBySigma[sigma]


			del rootsBySigma

		store(newRoots, DATA_FOLDER / f"roots/rootsBatch{rootsBatches}.dat")
		rootsBatches += 1

		print("rootsBatches: " + str(rootsBatches))

		del newRoots

		store(evens, DATA_FOLDER / f"evens/evens{d}.dat")
		del evens



# evens at depth, new nodes at depth, previous width, change in width
def expandSide (evensFolder, m, n, dM, dN):
	# print(f"\nPARENTS OF EVENS:\t\t{evenParents}")
	# evenParents = set(evenParents)
	# print("\nExpanding Side")
	# print(f"m: {m}")
	# print(f"n: {n}")
	# print(f"dM: {dM}")
	# print(f"dN: {dN}")

	roots = set()
	for x in range(m+1, m+dM + 1):
		roots.add((x,))
	# print(f"roots: {roots}\n")
	for d in range(2, n + 1):
		# print(f"d: {d}")
		roots = expandSideLayer(evensFolder, roots, d, m, dM)
		# print(f"roots: {roots}")

	# print("finished expandSide")
	return roots

def expandSideLayer(evensFolder, roots, depth, pM, dM):
	# print("ExpandingSideLayer")
	evens = load(evensFolder / f"evens{depth}.dat")
	# print(f"evens: {evens}")

	unknownNodes = []
	for root in roots:
		for x in range(1,root[-1]+1):
			unknownNodes.append(tuple(list(root) + [x]))
	unknownNodes.sort(key=sum)


	evenParents = set()
	for even in evens:
		evenParents.update(getParents(pM, dM, even))
	newRoots = set()
	for unknown in unknownNodes:
		# print(f"\nunkown: {unknown}")
		# print(f"parents of evens: {evenParents}")
		if unknown in evenParents:
			# print(f"adding {unknown} to newRoots")
			newRoots.add(unknown)
		else:
			evens.add(unknown)
			evenParents.update(getParents(pM, dM, unknown))

	store(evens, evensFolder / f"evens{depth}.dat")
	# print("finished side layer\n")
	return newRoots

# returns the parents of a node at depth (don't add the tails)
# pass in previous width, change in width, and the node
def getParents (pM, dM, evenNode):
	parents = set()
	layerEq = layerEquivalence(evenNode)
	lastAdded = set()

	for d in range(len(evenNode)):
		start = max(pM + 1, evenNode[0] + 1)
		stop = pM + dM + 1
		if d != 0:
			start = min(evenNode[d] + 1, pM + 1)
			stop = max(evenNode[d-1] + 1, start)
		if layerEq[d]:
			toAdd = set()
			for parent in lastAdded:
				for i in range(parent[d], parent[d-1] + 1):
					p = list(parent[:])
					p[d] = i
					toAdd.add(tuple(p))
			lastAdded.update(toAdd)
		else:
			parents.update(lastAdded)
			lastAdded = set()
		for i in range(start, stop):
			p = list(evenNode[:])
			p[d] = i
			lastAdded.add(tuple(p))
		parents.update(lastAdded)

	# print(f"pM: {pM}\ndM: {dM}")
	# print(f"parents of {evenNode}: {parents}")
	return parents

def layerEquivalence(path):
		layerEq = [False] * len(path)
		for i in range(1, len(path)):
			layerEq[i] = path[i] == path[i-1]
		return layerEq

def emptyDir(folder):
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

def load(fileName):
	with open (fileName, 'rb') as f:
		return pickle.load(f)

def store(data, fileName):
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)
