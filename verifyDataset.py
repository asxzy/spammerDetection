#!/usr/bin/env pypy
import io,sys

graph = {}
count = 0
missing = io.open('missing.log','wb')
private = io.open('private.log','wb')
log = io.open("log.log",'wb')
with io.open(sys.argv[1]) as f:
    for line in f:
        count += 1
        if count % 1000000 == 0:
            print count
        line = [int(x) for x in line.split()]
        try:
            graph[line[0]] += 1
        except KeyError:
            graph[line[0]] = 1

print "loaded"
print len(graph)
log.write(str(len(graph))+"\n")
with io.open(sys.argv[2]) as f:
    for line in f:
        line = line.split()
        line[0] = int(line[0])
        line[1] = int(line[1])
        line[2] = int(line[2])
        if line[1] == 0 or line[2] == 'True':
            continue
        try:
            graph[line[0]]
        except:
            if line[3] == 0:
                print line[0],"not crawled"
                log.write(str(line[0])+"not crawled\n")
            else:
                print line[0],"private"
                private.write(str(line[0])+"\n")
        try:
            if graph[line[0]] != line[1]:
                log.write("degree not match record "+str(line[0])+"\t"+str(line[1])+" crawled "+str(graph[line[0]])+"\n")
        except:
            missing.write(str(line[0])+"\n")
