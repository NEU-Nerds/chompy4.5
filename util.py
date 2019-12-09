import pickle

def expandDown(roots, m, n, dM, dN):
	evens = set()
	newRoots = set()

	rootsBySigma = []
	for i in range((m+dM)*(n+dN) + 1):
		rootsBySigma.append(set())
	#fill rootsBySigma
	# print("roots: " + str(roots))
	for root in roots:
		# print(f"root: {root}")
		for t in range(1, root[-1] + 1):
			# print("t: " +str(t))
			rootsBySigma[sum(root) + t].add(root)

	# print(f"rootsBySigma: {rootsBySigma}")
	# print("\n\n")
	for sigma in range(len(rootsBySigma)):
		# print(f"sigma: {sigma}")
		leaves = []
		for root in rootsBySigma[sigma]:
			# print(f"root: {root}")
			#all roots here will be even when we get to it
			#get the parents of the evens node,
			#create the parents
			#remove their branchNode from the corresponding rootsBySigma
			#go to the next root

			#create the node, add it to evens
			node = tuple(list(root) + [sigma - sum(root)] )
			# print(f"node: {node}")
			evens.add(node)

			#get the parents of node
			start = root[0]
			parents = getParents(start, dM, node)
			# print(f"parent: {parents}")

			#create the parent nodes, remove their root from rootsBySigma, add to newRoots
			for parent in parents:
				pRoot = parent[:-1]
				rootsBySigma[sum(parent)].discard(pRoot)
				newRoots.add(parent)
	print("finished expandDown\n")
	return evens, newRoots


# evens at depth, new nodes at depth, previous width, change in width
def expandSide (evensFolder, m, n, dM, dN):
	# print(f"\nPARENTS OF EVENS:\t\t{evenParents}")
	# evenParents = set(evenParents)
	print("\nExpanding Side")

	roots = set()
	for x in range(m+1, m+dM + 1):
		roots.add((x,))
	print(f"roots: {roots}\n")
	for d in range(2, n + 1):
		print(f"d: {d}")
		roots = expandSideLayer(evensFolder, roots, d, m, dM)
		print(f"roots: {roots}")

	print("finished expandSide")
	return roots

def expandSideLayer(evensFolder, roots, depth, pM, dM):
	print("ExpandingSideLayer")
	evens = load(evensFolder / f"evens{depth}.dat")
	print(f"evens: {evens}")

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
		print(f"\nunkown: {unknown}")
		print(f"parents of evens: {evenParents}")
		if unknown in evenParents:
			print(f"adding {unknown} to newRoots")
			newRoots.add(unknown)
		else:
			evens.add(unknown)
			evenParents.update(getParents(pM, dM, unknown))

	store(evens, evensFolder / f"evens{depth}.dat")
	print("finished side layer\n")
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

	print(f"pM: {pM}\ndM: {dM}")
	print(f"parents of {evenNode}: {parents}")
	return parents

def layerEquivalence(path):
		layerEq = [False] * len(path)
		for i in range(1, len(path)):
			layerEq[i] = path[i] == path[i-1]
		return layerEq

def load(fileName):
	with open (fileName, 'rb') as f:
		return pickle.load(f)

def store(data, fileName):
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)
