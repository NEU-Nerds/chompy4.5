import util
import settings
from pathlib import Path
settings.init()
N = 12


EVENS = set()
for x in range(1,N+1):
    eX = util.load(settings.EVENS_FOLDER / f"evens{x}.dat")
    EVENS.update(eX)

def genAllNodes(m,n):
    # print(f"genAllNodes: {m},{n}")
    for x in range(1,m+1):
        yield from genAllNodesRec(m,n, [x])
def genAllNodesRec(m,n,p):
    # print(f"genAllNodes: {m},{n}, {p}")
    if len(p) >= n:
        yield tuple(p)
    else:
        for x in range(p[-1]+1):
            if x == 0:
                yield tuple(p)
            else:
                yield from genAllNodesRec(m,n,p[:]+[x])

#winning moves dict
wMD = {}
mult = {}
byNum = {}
for node in genAllNodes(N, N):
    moves = []
    for c in util.getChildren(node):
        if c in EVENS:
            moves.append(c)
    wMD[node] = moves
    if len(moves) > 1:
        mult[node] = moves

    if len(moves) in byNum.keys():
        byNum[len(moves)].append(node)
    else:
        byNum[len(moves)] = [node]

# for key in mult.keys():
#     print(f"{key} \thas {len(mult[key])} moves")#:\t{mult[key]}")

print(byNum.keys())
for k in byNum.keys():
    print(f"{k}: {len(byNum[k])}")
