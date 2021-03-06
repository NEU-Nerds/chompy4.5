import _pickle as pickle
import os
import shutil
import time
import sys
# import json
import settings
# from objsize import get_deep_size


#eventually replace with trie if this takes time
#does take some time
#all prefixes will be tuples
def getPrefix(node, root):
	pS = settings.staticPrefixes
	if root:
		pS = settings.prefixes

	index = 0
	while index <= len(node):
		if node[:index] in pS:
			return node[:index]
		index += 1
	return (node[0],)

#only split newRoots
def splitPrefix(prefix, s):
	# print(f"Splititng pre: {s}")
	# print(f"Splititng preP: {settings.prefixes}")
	for t in range(1, prefix[-1]+1):
		settings.prefixes.add(prefix + (t,))
	settings.prefixes.remove(prefix)

	nodes = s[prefix]
	# print(f"nodes: {nodes}")
	del s[prefix]
	# print(f"Splititng mid: {s}")
	for node in nodes:
		addToSet(node, s, True)#, maxNodes)


	#for file in oldPrefix dir, load nodes and store into current dir
	try:
		# print(os.listdir(settings.currRootsDir))
		for f in os.listdir(settings.currRootsDir / f"{prefix}/"):
			try:
				roots = load(settings.currRootsDir / f"{prefix}/{f}")
				# print(f"loaded roots: {roots}")
				for root in roots:
					addToSet(root, s, True)
			except OSError as e:
				# print(f"could not load {prefix} with e: {e}")
				pass
	except Exception as e:
		# print(f"splitPrefix error: {e}")
		pass

	# print(f"post s: {s}")

# def addPrefix(p):
# 	index = 0
#
# 	currList = settings.prefixes
# 	while index < len(p) and p[index] in currList:
# 		index += 1




def addToSet(node, s, root=False):
	p = getPrefix(node, root)

	if p in s.keys():
		s[p].add(node)
	else:
		s[p] = set([node])

	if root and len(s[p]) > settings.MAX_ROOTS:
		splitPrefix(p, s,)


#RBS is the roots of the new nodes indexed by the sigma of the node
#Note a root = node[:-1]
def genRBS(roots):
	rootsBySigma = {}
	for root in roots:
		#t = addition to root's path to create the node
		for t in range(1, root[-1] + 1):
			key = sum(root) + t
			if key in rootsBySigma.keys():
				rootsBySigma[key].add(root)
			else:
				rootsBySigma[key] = set([root])
				# keys.add(key)
	# if log:
		# print(f"Size of RBS: {sys.getsizeof(rootsBySigma)}")
		# print(f"Deep RBS objSize: {get_deep_size(rootsBySigma)}")
	return rootsBySigma

#get the parents of the existing evens and store them in parents directory
def genParentsFromExistingEvens(evens, depth, pM, dM):
	# print("genParentsFromExistingEvens")
	workingParents = set()
	settings.currParentsNum = 0
	# print(f"pM: {pM}\tdM: {dM}")
	for even in evens:
		getParents(pM, dM, even, workingParents, {}, {})
		# getParents(pM, dM, even, workingParents, {}, {})
	storeParents(workingParents)
	# for pfix in workingParents.keys():
	# 	try:
	# 		dirStore(workingParents[pfix], settings.PARENTS_FOLDER, str(pfix))
	# 		# print(f"storing pfix: {pfix}:\t{workingParents[pfix]}")
	# 	except Exception as e:
	# 		# print("could not store bc: "+str(e))
	# 		pass


def addParent(p, parents, rBS, newRoots):
	# if p == (6, 1, 1, 1, 1):
	# 	print("(6, 1, 1, 1, 1) was a parent")
	# pRoot =
	# print(f"PARENT: {p} from node {e}" )
	try:
		rBS[sum(p)].remove(p[:-1])
		# print(f"adding new root: {p}")
		addToSet(p, newRoots, root=True)
	except Exception as e:
		# print(f"addParent error: {e}")
		pass

	parents.add(p)
	if len(parents) > settings.MAX_ROOTS:
		storeParents(parents)


	"""
	#what about repeates? Ignore for now?
	# if p not in parents
	addToSet(p, parents)
	settings.currParentsNum += 1

	# s = 0
	# for k in parents.keys():
	# 	s += len(parents[k])
	if settings.currParentsNum > settings.MAX_ROOTS:
		# print(f"storing parents from addParent: {parents}")
		for prefix in parents.keys():
			try:

				dirStore(parents[prefix], settings.PARENTS_FOLDER, str(prefix))
			except Exception as e:
				# print(f"in addParent could not store bc: {e}")
				pass
		settings.currParentsNum = 0
		parents.clear()
	"""
# returns the parents of a given node at the same tree depth (don't add the tails)
# pass in previous width, change in width, and the node
def getP(p, pM, dM):
	lE= layerEquivalence(p)
	# print(f"lE: {lE}")
	if p[0] > pM:
		yield from recP(list(p)[:], lE, True, 1)
	for x in range(max(p[0],pM+1), pM+dM+1):
		# print(f"x: {x}")
		wP = list(p)[:]
		wP[0] = x
		if x != p[0]:
			yield tuple(wP)
		yield from recP(wP, lE, False, 1)



def recP(wP, lE, untouched, i):
	# untouched = copy(untouched)
	wP = wP[:]
	# print(f"RecP call with: {wP}, {lE}, {untouched}, {i}")
	if i >= len(wP):
		# print("HELLO")
		return


	# if i < len(wP)-1 or not untouched:
	yield from recP(wP, lE, untouched, i+1)

	# for i in range(startI, len(wP)):
		# yield from recP(wP, i+1)
	if untouched:
		untouched = False
		for x in range(wP[i]+1, wP[i-1]+1):
			wP[i] = x
			# print(f"yielding {wP}")
			yield tuple(wP)
			yield from recP(wP, lE, untouched, i+1)
	elif lE[i]:
		# print("HI")
		untouched = False
		for x in range(wP[i]+1, wP[i-1]+1):
			wP[i] = x
			# print(f"yielding {wP}")
			yield tuple(wP)
			yield from recP(wP, lE, untouched, i+1)


def getParents (pM, dM, evenNode, parents, rBS, newRoots):
	for p in getP(evenNode, pM, dM):
		# print(f"parent: {p}")
		addParent(p, parents, rBS, newRoots)
	# for prefix in parents.keys():
	# 	try:
	# 		dirStore(parents[prefix], folder, str(prefix))
	# 	except Exception as e:
	# 		print(f"error: {e}")
	# 	parents.clear()
"""
def getParents2 (pM, dM, evenNode, parents, rBS, newRoots):
	# parents = {} # stores all generated parents of the even node, eventually returned
	lastAdded = set() # used to store things between depths for layer equivalence stuff
	layerEq = layerEquivalence(evenNode)
	tempParents = set()
	# redCount = 0
	# totalCount = 0
	# go through each index of the node
	for d in range(len(evenNode)):
		# finding the range of numbers that can be parents
			# set "start" and "stop" depending on the depth
				# start at the max of 1 greater than the current width or 1 more than the int at current depth
			# if depth is 0:
				# stop at the next width + 1
			# if depth is not 0:
				# stop at the max of (start or int at previous depth +1)

		start = max(pM + 1, evenNode[d] + 1)
		# stop = dM + 1
		stop = newM + 1
		if d != 0:
			# start = min(evenNode[d] + 1, pM + 1)
			stop = max(evenNode[d-1] + 1, start)

		# the value of the parent at any depth must be greater than or equal to the value of the child at any depth
		 	# this is why we start is set to be evenNode[d] + 1.
			# we add in the max of that and previous width so we don't have to
				# generate the parents of the even board that have already been generated
		# the upper limit is different depending on whether depth is 0 or not 0.
			# if depth is 0, the upper limit is simply the new width (+ 1 so it's inclusive)
			# if depth is not 0, the upper limit should be the previous depth's value (+1 for inclusive)
				# however if that is less than the value of start, we don't want to do anything at this depth
				# so we use the max() with start. eg: "for i in range(foo, foo)" does nothing

		# see if the last layer is the same as this layer
		if layerEq[d]:
			toAdd = set() #1 new parents to be added to the overall list later
			for parent in lastAdded: # go through all of the parents from the previous layer(s)
				# add new parents based off of the current parent for every possible value
				# the new parents can be from the value of the current depth to the value of previous depth
				for i in range(parent[d], parent[d-1] + 1):
					p = list(parent[:])
					p[d] = i

					toAdd.add(tuple(p))
			lastAdded.update(toAdd)
		else:
			for p in lastAdded:
				addParent(p, parents, rBS, newRoots)
				if p in tempParents:
					# print(f"Redundent parent: {p}")
					settings.redCount += 1
					settings.totalCount += 1
				else:
					tempParents.add(p)
					settings.totalCount += 1
			# parents.update(lastAdded) # add the parents from last added to the list of parents
			lastAdded = set() # reset lastAdded because the layers are different

		# setting the nodes in the range of previously generated numbers as parents
		for i in range(start, stop):
			# casting to list from tuple so you can change the value at the current depth
			p = list(evenNode[:]) # copy the current node
			p[d] = i #change the value at current depth
			lastAdded.add(tuple(p))
		for p in lastAdded:
			addParent(p, parents, rBS, newRoots)
			if p in tempParents:
				# print(f"Redundent parent: {p}")
				settings.redCount += 1
				settings.totalCount += 1
			else:
				tempParents.add(p)
				settings.totalCount += 1
		# parents.update(lastAdded)

	# return parents
	# for prefix in parents.keys():
	# 	try:
	# 		dirStore(parents[prefix], folder, str(prefix))
	# 	except Exception as e:
	# 		print(f"error: {e}")
	# parents.clear()
	# print(f"Total count: {totalCount}\tRedundantCount: {redCount}\tratio: {redCount/totalCount}")
	# if totalCount >= 5000000:
	# 	print(f"Biggun: {evenNode}")
#mostly identical to getParents, but without all the extra stuff for batching so it can be tested easily
def getParentsTest (pM, newM, evenNode):
	parents = set() # stores all generated parents of the even node, eventually returned
	lastAdded = set() # used to store things between depths for layer equivalence stuff
	layerEq = layerEquivalence(evenNode)

	# go through each index of the node
	for d in range(len(evenNode)):
		# finding the range of numbers that can be parents
			# set "start" and "stop" depending on the depth
				# start at the max of 1 greater than the current width or 1 more than the int at current depth
			# if depth is 0:
				# stop at the next width + 1
			# if depth is not 0:
				# stop at the max of (start or int at previous depth +1)

		start = max(pM + 1, evenNode[d] + 1)
		stop = newM + 1
		if d != 0:
			# start = min(evenNode[d] + 1, pM + 1)
			stop = max(evenNode[d-1] + 1, start)

		# the value of the parent at any depth must be greater than or equal to the value of the child at any depth
		 	# this is why we start is set to be evenNode[d] + 1.
			# we add in the max of that and previous width so we don't have to
				# generate the parents of the even board that have already been generated
		# the upper limit is different depending on whether depth is 0 or not 0.
			# if depth is 0, the upper limit is simply the new width (+ 1 so it's inclusive)
			# if depth is not 0, the upper limit should be the previous depth's value (+1 for inclusive)
				# however if that is less than the value of start, we don't want to do anything at this depth
				# so we use the max() with start. eg: "for i in range(foo, foo)" does nothing

		# see if the last layer is the same as this layer
		if layerEq[d]:
			toAdd = set() #1 new parents to be added to the overall list later
			for parent in lastAdded: # go through all of the parents from the previous layer(s)
				# add new parents based off of the current parent for every possible value
				# the new parents can be from the value of the current depth to the value of previous depth
				for i in range(parent[d], parent[d-1] + 1):
					p = list(parent[:])
					p[d] = i

					toAdd.add(tuple(p))
			lastAdded.update(toAdd)
		else:
			# for p in lastAdded:
				# addParent(p, parents, rBS, newRoots, prefixes, oldPrefixes, folder, MAX_ROOTS, evenNode, toPrint)
			parents.update(lastAdded) # add the parents from last added to the list of parents
			lastAdded = set() # reset lastAdded because the layers are different

		# setting the nodes in the range of previously generated numbers as parents
		for i in range(start, stop):
			# casting to list from tuple so you can change the value at the current depth
			p = list(evenNode[:]) # copy the current node
			p[d] = i #change the value at current depth
			lastAdded.add(tuple(p))
		# for p in lastAdded:
			# addParent(p, parents, rBS, newRoots, prefixes, oldPrefixes, folder, MAX_ROOTS, evenNode, toPrint)
		parents.update(lastAdded)

	return parents
	# for prefix in parents.keys():
	# 	try:
	# 		dirStore(parents[prefix], folder, str(prefix))
	# 	except Exception as e:
	# 		print(f"error: {e}")
	# parents.clear())
"""

# pass in a path representing a node.
# returns a list of bools with the same length
# the bool at each index represents whether the int at the index - 1 and the index are the same
# index 0 is always false
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

def storeParents(parents):
	sortedP = {}
	for p in parents:
		addToSet(p, sortedP)

	for pfix in sortedP.keys():
		try:
			dirStore(sortedP[pfix], settings.PARENTS_FOLDER, str(pfix))
		except Exception as e:
			# print(f"error: {e}")
			pass
	parents.clear()

def dirStore(data, folder, name):
	try:
		os.mkdir(folder / name)
	except:
		pass
	# if os.path.isdir(folder / name):
	# print(f"contents: {os.listdir(folder / name)}")
	path1 = folder / name / f"{(len(os.listdir(folder / name)))}.dat"
	# print(f"storing {path1}")
	store(data, path1)
	# else:

		# store(data, folder / name / "0.dat")

def multiCombineWrapper(x):
	combineDir(x[0],x[1])

def combineDir(folder, name, combine=False):
	# print(f"combining {folder / name}")
	all = set()
	try:
		for f in os.listdir(folder / name):
			all.update(load(folder / name / f))
		if combine:
			try:
				all.update(load(folder / (name + ".dat")))
			except:
				pass
		shutil.rmtree(folder / name)
		store(all, folder / (name + ".dat"))
	except:
		# print(f"failed {folder} / {name}")
		pass

# def evensLoad(x):
# 	return load(x)
#
# def rootsLoad(x):
# 	return load(x)

def load(fileName):
	with open (fileName, 'rb') as f:
		return pickle.load(f)

# def rootsStore(x1, x2):
# 	store(x1, x2)

def store(data, fileName):
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)
"""
def load(fileName, isSet=True):
	with open(fileName, "r") as file:
		jData = file.read()
		# +" "
		# jData = "[" + jData[1:-1]
		data = json.loads(jData)
		try:
			if isSet:
				data = set(data)
		except:
			print(f"data: {data}\tfileName: {fileName}")

			exit()
		return data

def store(data, fileName):
	with open(fileName, "w") as file:
		jData = json.dumps(list(data))
		file.write(jData)
		# file.write(str(data))
		# return 1
"""
