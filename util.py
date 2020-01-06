import pickle
import os
import shutil
import time
import sys
# from objsize import get_deep_size

def addToNewRoots(node, newRoots, batchDepth):
	if len(node) > batchDepth:
		p = tuple(node[:len(node)-batchDepth])
	else:
		p = 0

	if p in newRoots.keys():

		newRoots[p].add(node)
	else:
		newRoots[p] = set([node])


#RBS is the roots of the new nodes indexed by the sigma of the node
#Note a root = node[:-1] (I love how this looks like a face btw)
def genRBS(roots, log=False):
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
def genParentsFromExistingEvens(DATA_FOLDER, evens, depth, pM, dM, maxDepth):


	#sort evensL so that lowest sigma first, so we can store parents of sigmas we're done with
	evensL = list(evens)
	evensL.sort(key=sum)

	#dict of parents by sigma
	parentsDict = {}
	for even in evensL:
		#get parents of even and add to parentsDict
		parents = getParents(pM, dM, even)
		for parent in parents:

			if len(parent) > maxDepth:
				pPrefix = tuple(parent[:len(parent)-maxDepth])
			else:
				pPrefix = 0
			if pPrefix in parentsDict.keys():
				parentsDict[pPrefix].add(parent)
			else:
				parentsDict[pPrefix] = set([parent])

	#BATCH??
	for p in parentsDict.keys():
		try:
			oldParents = load(DATA_FOLDER / f"parents/{str(p)}.dat")
			combParents = oldParents.union(parentsDict[p])
			del oldParents

		except OSError:
			combParents = parentsDict[p]
		# print(f"p: {p}")
		store(combParents, DATA_FOLDER / f"parents/{str(p)}.dat")


	del evensL
	#store parents of any sigmas leftover
	# for k in parentsDict.keys(): #range(min(parentsDict.keys()), max(parentsDict.keys()) +1):
	# 	# print(f"storing k of {k}")
	#
	# 	#merge with existing parents
	# 	try:
	# 		prevParents = load(DATA_FOLDER / f"parents/parentsSigma{k}.dat")
	# 	except:
	# 		prevParents = None
	#
	# 	if prevParents:
	# 		combParents = prevParents.union(parentsDict[k])
	# 		del prevParents
	# 	else:
	# 		combParents = parentsDict[k]
	#
	# 	store(combParents, DATA_FOLDER / f"parents/parentsSigma{k}.dat")
	#
	# 	del prevParents
	# 	del combParents

	del parentsDict

# returns the parents of a given node at the same tree depth (don't add the tails)
# pass in previous width, change in width, and the node
def getParents (pM, dM, evenNode):
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

		start = max(pM, evenNode[d] + 1)
		stop = pM + dM + 1
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
			toAdd = set() # new parents to be added to the overall list later
			for parent in lastAdded: # go through all of the parents from the previous layer(s)
				# add new parents based off of the current parent for every possible value
				# the new parents can be from the value of the current depth to the value of previous depth
				for i in range(parent[d], parent[d-1] + 1):
					p = list(parent[:])
					p[d] = i
					toAdd.add(tuple(p))
			lastAdded.update(toAdd)
		else:
			parents.update(lastAdded) # add the parents from last added to the list of parents
			lastAdded = set() # reset lastAdded because the layers are different

		# setting the nodes in the range of previously generated numbers as parents
		for i in range(start, stop):
			# casting to list from tuple so you can change the value at the current depth
			p = list(evenNode[:]) # copy the current node
			p[d] = i #change the value at current depth
			lastAdded.add(tuple(p))
		parents.update(lastAdded)

	return parents

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

def load(fileName):
	with open (fileName, 'rb') as f:
		return pickle.load(f)

def store(data, fileName):
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)
