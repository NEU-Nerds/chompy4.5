import pickle
import os
import shutil
import time
import sys
from objsize import get_deep_size

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
	if log:
		# print(f"Size of RBS: {sys.getsizeof(rootsBySigma)}")
		print(f"Deep RBS objSize: {get_deep_size(rootsBySigma)}")
	return rootsBySigma

#get the parents of the existing evens and store them in parents directory
def genParentsFromExistingEvens(DATA_FOLDER, evens, depth, pM, dM):


	#sort evensL so that lowest sigma first, so we can store parents of sigmas we're done with
	evensL = list(evens)
	evensL.sort(key=sum)

	#dict of parents by sigma
	parentsDict = {}
	for even in evensL:
		#get parents of even and add to parentsDict
		parents = getParents(pM, dM, even)
		for parent in parents:
			sigma = sum(parent)
			if sigma in parentsDict.keys():
				parentsDict[sigma].add(parent)
			else:
				parentsDict[sigma] = set([parent])

		#Store parents of all keys that are less than any possible parent yet to be generated
		for k in range(min(parentsDict.keys()), sum(even) + 1):

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

			store(combParents, DATA_FOLDER / f"parents/parentsSigma{k}.dat")

			del prevParents
			del combParents
			del parentsDict[k]
	del evensL
	#store parents of any sigmas leftover
	for k in parentsDict.keys(): #range(min(parentsDict.keys()), max(parentsDict.keys()) +1):
		# print(f"storing k of {k}")

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

		store(combParents, DATA_FOLDER / f"parents/parentsSigma{k}.dat")

		del prevParents
		del combParents

	del parentsDict

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
