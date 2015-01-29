#!/usr/bin/env pypy
import io
import sys

infos = {}
with io.open('innerLoopSpammer.log') as f:
    for line in f:
        line = line.split()
        try:
            infos[int(line[0])]
        except:
            infos[int(line[0])] = []
        infos[int(line[0])].append((line[2],line[4],line[6],line[8]))
for info in sorted(infos.keys()):
    A = []
    B = []
    for info in infos[info]:
        try:
            a = 1.0*float(info[0])/float(info[2])
        except:
            a = 0
        try:
            b = 1.0*float(info[1])/float(info[3])
        except:
            b = 0
        a = int(info[0])
        b = int(info[1])
        A.append(a)
        B.append(b)
    #print info+1,"&","{:.3f}".format(100.*sum(avg)/len(avg)),'\% \\\\'
    print "{:.3f}".format(100.*sum(A)/len(A)),"&","{:.3f}".format(100.*sum(B)/len(B))#,'\\\\'
