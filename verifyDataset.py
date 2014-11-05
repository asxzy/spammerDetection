#!/usr/bin/env python
import io,sys

graph = {}
with io.open(sys.argv[1]) as f:
    for line in f:
        line = [int(x) for x in line.split()]
        try:
            graph[line[0]] += 1
        except KeyError:
            graph[line[0]] = 1

private = []
missing = []
degree = []
with io.open(sys.argv[2]) as f:
    for line in f:
        line = [int(x) for x in line.split()]
        try:
            graph[line[0]]
        except:
            if line[3] == 0:
                print line[0],"not crawled"
                missing.append(line[0])
            else:
                print line[0],"private"
                private.append(line[0])
        if graph[line[0]] != line[1]:
            degree[line[0]] = (graph[line[0]],line[1])
            print "degree not match","record",line[1],"crawled",graph[line[0]]

