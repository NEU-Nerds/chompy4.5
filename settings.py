import os
from pathlib import Path

THIS_FOLDER = None
THIS_FOLDER = None
DATA_FOLDER = None
EVENS_FOLDER = None
ROOTS_FOLDER = None
PARENTS_FOLDER = None
ROOTS_BY_SIGMA_FOLDER = None

MAX_M = None
MAX_N = None

#currently only do 1
DELTA_N = None
DELTA_M = None

#The maximum # of roots in one batch, eventually change to be dependent on
#the length of roots so memory use is constant
# MAX_ROOTS = 10 ** 6
MAX_ROOTS = None

DATA_FOLDER = None
prefixes = None
staticPrefixes = None
currRootsDir = None
currOldRootsDir = None
currParentsNum = None

printEvens = None
doSeed = None

redCount = None
totalCount = None


rootCount = None
totalRootCount = None

def init():
    global THIS_FOLDER
    global THIS_FOLDER
    global DATA_FOLDER
    global EVENS_FOLDER
    global ROOTS_FOLDER
    global PARENTS_FOLDER
    global ROOTS_BY_SIGMA_FOLDER
    global MAX_M
    global MAX_N
    global DELTA_N
    global DELTA_M
    global MAX_ROOTS
    global printEvens
    global doSeed
    global currParentsNum

    global redCount
    global totalCount

    global rootCount
    global totalRootCount


    redCount = 0
    totalCount = 0

    currParentsNum = 0

    rootCount = 0
    totalRootCount = 0

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    #THIS_FOLDER = "D:/Mass Storage/Math/chompy"
    # THIS_FOLDER = "/Users/tymarking/Documents/chomp/chompy4"
    # print(THIS_FOLDER)
    THIS_FOLDER = Path(THIS_FOLDER)
    DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc5/")
    EVENS_FOLDER = Path(DATA_FOLDER, "./evens/")
    ROOTS_FOLDER = Path(DATA_FOLDER, "./rootBatches/")
    PARENTS_FOLDER = Path(DATA_FOLDER, "./parents/")
    ROOTS_BY_SIGMA_FOLDER = Path(DATA_FOLDER, "./rootsBySigma/")

    MAX_M = 10
    MAX_N = 10

    doSeed = True

    #currently only do 1
    DELTA_N = 1
    DELTA_M = 1

    #The maximum # of roots in one batch, eventually change to be dependent on
    #the length of roots so memory use is constant
    MAX_ROOTS = 10 ** 6
    # MAX_ROOTS = 5

    # printEvens = True
