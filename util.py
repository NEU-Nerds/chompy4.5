

def expandDown(roots, m, n, dM, dN):
	evens = set()
	newRoots = set()

	rootsBySigma = []
	for i in range(m*n + 1):
		rootsBySigma.append(set())
	#fill rootsBySigma
	# print("roots: " + str(roots))
	for root in roots:
		# print(f"root: {root}")
		for t in range(1, root[-1] + 1):
			# print("t: " +str(t))
			rootsBySigma[root.node.sigma + t].add(root)

	# print(f"rootsBySigma: {rootsBySigma}")
	# print("\n\n")
	for sigma in range(len(rootsBySigma)):
		# print(f"sigma: {sigma}")
		leaves = []
		for root in rootsBySigma[sigma]:
			#all roots here will be even when we get to it
			#get the parents of the evens node,
			#create the parents
			#remove their branchNode from the corresponding rootsBySigma
			#go to the next root

			#create the node, add it to evens
			node = tuple(list(root).append(sigma - sum(root)))
			evens.add(node)

			#get the parents of node
			start = root[0]
			parents = getParents(start, m-start, root)

			#create the parent nodes, remove their root from rootsBySigma, add to newRoots
			for parent in parents:
				pRoot = parent[:-1]
				rootsBySigma[sum(parent)].discard(pRoot)
				newRoots.add(parent)

	return evens, newRoots



# evens at depth, new nodes at depth, previous width, change in width
def expandSide (evensFolder, pM, dM, pN, dN):

	evens = load(evensFolder / f"evens{pN}.dat")


	evenParents = set()
	for even in evens:
		evenParents.extend(getParents(pM, dM, even))
	# print(f"\nPARENTS OF EVENS:\t\t{evenParents}")
	# evenParents = set(evenParents)

	roots = set()
	for unknown in uncheckedNodes:
		# print(f"parents of evens: {evenParents}")
		if path in evenParents:
			unknown.setOdd()
			roots.update(unknown)
		else:
			unknown.setEven()
			evens.add(unknown)
			evenParents.update(getParents(pM, dM, unknown))

	# print("DONE WITH PARENTS\n\n")
	return roots

# returns the parents of a node at depth (don't add the tails)
# pass in previous width, change in width, and the node
def getParents (pM, dM, evenNode):
	parents = set()

	# maybe use layerEquivalence to do this?
	layerEq = evenNode.layerEquivalence()

	lastAdded = set()

	for d in range(len(path)):
		start = max(pM + 1, path[0] + 1)
		stop = pM + dM + 1
		if d != 0:
			start = min(path[d] + 1, pM + 1)
			stop = max(path[d-1] + 1, start)
		if layerEq[d]:
			toAdd = set()
			for parent in lastAdded:
				for i in range(parent[d], parent[d-1] + 1):
					p = list(parent[:])
					p[d] = i
					toAdd.extend(tuple(p))
			lastAdded.update(toAdd)
		else:
			parents.update(lastAdded)
			lastAdded = []
		for i in range(start, stop):
			p = list(path[:])
			p[d] = i
			# parents[-1][d] = i
			lastAdded.update(tuple(p))
	parents.update(lastAdded)
	# for d in range(1, len(evenNode.path)):

	# print(f"pN: {pN}\ndN: {dN}")
	# print(f"parents of {evenNode.node}: {parents}")
	return tuple(parents)


def load(fileName):
	with open (fileName, 'rb') as f:
		return pickle.load(f)

def store(data, fileName):
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)
