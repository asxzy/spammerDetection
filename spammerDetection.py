#!/usr/bin/env pypy
from funcs import *
import sys


if __name__ == '__main__':
    data = sys.argv[1]
    #print "node list"
    #findNodeList(data)
    #print "node degree"
    #findNodeDegree(data)
    #print "seed"
    #findSeedList(data)
    #print "seed degree"
    #findSeedDegree(data)
    print "filter JS"
    findJS(data)
    print "ND"
    findNearDuplicates(data)
    print "spammer"
    findSpammers(data)
    print "ndjs"
    findNearDuplicatesJS(data)
