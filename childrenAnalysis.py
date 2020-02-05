import util

def genAllNodes(m,n):
    # print(f"genAllNodes: {m},{n}")
    for x in range(1,m+1):
        yield from genAllNodesRec(m,n, [x])
def genAllNodesRec(m,n,p):
    # print(f"genAllNodes: {m},{n}, {p}")
    if len(p) >= n:
        yield p
    else:
        for x in range(p[-1]+1):
            if x == 0:
                yield p
            else:
                yield from genAllNodesRec(m,n,p[:]+[x])

def getChildren(node):

    pass

for node in genAllNodes(4,5):
    print(node)
