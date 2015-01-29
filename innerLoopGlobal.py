#!/usr/bin/env pypy
import io
import sys

infos = {}
with io.open('innerLoopGlobal.log') as f:
    for line in f:
        line = line.split()
        try:
            infos[int(line[0])]
        except:
            infos[int(line[0])] = []
        infos[int(line[0])].append((line[2],line[4],line[6]))
A = []
B = []
loop = 0
inDeg = 0
for info in sorted(infos.keys()):
    info = infos[info][0]
    #loop += int(a[0])
    #inDeg += int(a[1])
    try:
        a = 1.0*float(info[0])/float(info[1])
    except:
        a = 0
    try:
        b = 1.0*float(info[0])/float(info[2])
    except:
        b = 0
    A.append(a)
    B.append(b)
print "global",1.0*sum(A)/len(A),1.0*sum(B)/len(B)
