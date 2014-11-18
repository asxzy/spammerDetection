#!/usr/bin/env python
from funcs import *


if __name__ == '__main__':
    data = sys.argv[1]
    print "cluster"
    findCluster(data,showPlot=True)
