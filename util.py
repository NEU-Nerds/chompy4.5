import pickle
import os
import shutil
import time

MAX_ROOTS = 10 ** 6

def expandDown(DATA_FOLDER, m, n, dM, dN):
	for d in range(n+1, n+dN + 1):
		print(f"\nExpandingDown d = {d}")

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
			print(f"rootsBatch {i} with {len(roots)} roots")
			print("generating RBS")
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


			print("doing sigmas")
			for sigma in range(minSigma, maxSigma + 1):


				storeParents = set()

				#if this sigma is empty
				if sigma not in keys:
					# print("nothing here")
					continue
				# print(f"Sigma: {sigma}")
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

						# print(f"Node parent: {parent}")
						# print(f"rootsBySigma: {rootsBySigma}")
						#if greater than maxSigma then don't bother
						if sum(parent) <= maxSigma:
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

		# print("rootsBatches: " + str(rootsBatches))

		del newRoots

		store(evens, DATA_FOLDER / f"evens/evens{d}.dat")
		del evens
	print("finished all down expand")



# evens at depth, new nodes at depth, previous width, change in width
def expandSide (DATA_FOLDER, m, n, dM, dN):
	# print(f"\nPARENTS OF EVENS:\t\t{evenParents}")
	# evenParents = set(evenParents)
	print("\nExpanding Side")
	# print(f"m: {m}")
	# print(f"n: {n}")
	# print(f"dM: {dM}")
	# print(f"dN: {dN}")

	roots = set()
	for x in range(m+1, m+dM + 1):
		roots.add((x,))
	# print(f"roots: {roots}\n")
	store(roots, DATA_FOLDER / "sideRoots/rootsBatch0.dat")

	for d in range(2, n + dN):
		# print(f"d: {d}")
		expandSideLayer(DATA_FOLDER, d, m, dM)

	#take resulting side roots and add them to main roots
	numRootBatches = len(os.listdir(DATA_FOLDER / "roots"))
	for i in range(len(os.listdir(DATA_FOLDER / "sideRoots"))):
		# print(f"renaming side{i} to side{i+numRootBatches}")
		os.rename(DATA_FOLDER / f"sideRoots/rootsBatch{i}.dat", DATA_FOLDER / f"roots/rootsBatch{numRootBatches+i}.dat")
	print("finished expandSide")

def expandSideLayer(DATA_FOLDER, depth, pM, dM):
	print("ExpandingSideLayer d = " +str(depth))

	emptyDir(DATA_FOLDER / "parents")
	emptyDir(DATA_FOLDER / "sideOldRoots")

	os.rename(DATA_FOLDER / "sideOldRoots", DATA_FOLDER / "sideRootsTEMP")
	os.rename(DATA_FOLDER / "sideRoots", DATA_FOLDER / "sideOldRoots")
	os.rename(DATA_FOLDER / "sideRootsTEMP", DATA_FOLDER / "sideRoots")

	# evens = load(evensFolder / f"evens{depth}.dat")

	evens = load(DATA_FOLDER / f"evens/evens{depth}.dat")
	# print(f"evens: {evens}")
	#max = MAX_ROOTS
	newRoots = set()
	rootsBatches = 0

	#get the parents of the existing evens and store them in parents directory
	# (maybe we should keep this data around)
	evensL = list(evens)
	#sort evensL so that lowest sigma first, so we know groups of sigma's that we are done with
	evensL.sort(key=sum)
	# print(f"evensL: {evensL}")
	parentsDict = {}
	for even in evensL:
		# print(f"even: {even}")
		parents = getParents(pM, dM, even)

		for parent in parents:
			sigma = sum(parent)
			if sigma in parentsDict.keys():
				parentsDict[sigma].add(parent)
			else:
				parentsDict[sigma] = set([parent])
		#all keys that are less than any possible parent yet to be generated
		# print(f"parentsDict: {parentsDict}")
		# print(f"min parentsDict.keys(): {min(parentsDict.keys())}")
		for k in range(min(parentsDict.keys()), sum(even) + 1):
			# print(f"INSDIE storing k of {k}")

			if k not in parentsDict.keys():
				continue
			#merge with existing parents
			try:
				prevParents = load(DATA_FOLDER / f"parents/parentsSigma{k}.dat")
			except:
				prevParents = None

			if prevParents:
				combParents = prevParents.union(parentsDict[k])
				del prevParents
			else:
				combParents = parentsDict[k]
			# print(f"combParents: {combParents}")
			store(combParents, DATA_FOLDER / f"parents/parentsSigma{k}.dat")

			del prevParents
			del combParents
			del parentsDict[k]
	for k in range(min(parentsDict.keys()), max(parentsDict.keys()) +1):
		# print(f"storing k of {k}")

		if k not in parentsDict.keys():
			continue
		#merge with existing parents
		try:
			prevParents = load(DATA_FOLDER / f"parents/parentsSigma{k}.dat")
		except:
			prevParents = None

		if prevParents:
			combParents = prevParents.union(parentsDict[k])
			del prevParents
		else:
			combParents = parentsDict[k]
		# print(f"combParents: {combParents}")
		store(combParents, DATA_FOLDER / f"parents/parentsSigma{k}.dat")

		del prevParents
		del combParents
		del parentsDict[k]
	#put into parents dat files instead of memory

	# print("finished init evenParents")
	# print(f"init EvenParents: {evenParents}" )
	#load each root batch
	numRootBatches = len(os.listdir(DATA_FOLDER / "sideOldRoots"))
	for i in range(numRootBatches):
		roots = load(DATA_FOLDER / f"sideOldRoots/rootsBatch{i}.dat")

		# unknownNodes = []
		# for root in roots:
		# 	for x in range(1,root[-1]+1):
		# 		unknownNodes.append(tuple(list(root) + [x]))
		# unknownNodes.sort(key=sum)

		rootsBySigma = {}
		keys = set()
		for root in roots:
			# print(f"root: {root}")
			# print(f"preRootsBySigma: {rootsBySigma}")
			for t in range(1, root[-1] + 1):
				# print("t: " +str(t))
				# if (root + (t,)) in evenParents:
				# 	newRoots.add(root + (t,))
				# 	continue

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

			#if this sigma is empty
			if sigma not in keys:
				# print("nothing here")
				continue
			storeParents = set()
			# print(f"Sigma: {sigma}")
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
						store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
						rootsBatches += 1
						newRoots.clear()
						# print(f"newRoots post clear: {newRoots}")


			except OSError as e:
				prevParents = None
				# print("prev parents error : " + str(e))

			# print(f"postRootsBySigma: {rootsBySigma[sigma]}")

			for root in rootsBySigma[sigma]:
				#create the node, add it to evens
				node = tuple(list(root) + [sigma - sum(root)] )
				# print(f"node: {node}")

				#add maxEvens?
				evens.add(node)

				#get the parents of node
				start = root[0]
				parents = getParents(start, (pM)-start, node)
				# print(f"parents: {parents}")

				#create the parent nodes, remove their root from rootsBySigma, add to newRoots
				for parent in parents:

					# print(f"Node parent: {parent}")
					# print(f"rootsBySigma: {rootsBySigma}")
					#if greater than maxSigma then don't bother
					if sum(parent) <= maxSigma:
						pRoot = parent[:-1]
						try:
							rootsBySigma[sum(parent)].remove(pRoot)
							newRoots.add(parent)
							# print("added parent to newRoots")
						except:
							pass
						if len(newRoots) >= MAX_ROOTS:
							# print("STORING NEW ROOTS")
							store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
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

	store(newRoots, DATA_FOLDER / f"sideRoots/rootsBatch{rootsBatches}.dat")
	rootsBatches += 1

	# print("rootsBatches: " + str(rootsBatches))

	del newRoots
	# del evenParents
	store(evens, DATA_FOLDER / f"evens/evens{depth}.dat")
	del evens



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
