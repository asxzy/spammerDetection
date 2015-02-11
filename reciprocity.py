#!/usr/bin/env python
import io
import sys

a = {}
b = {}
with io.open('reciprocity.log') as f:
    f.readline()
    for line in f:
        line = [int(x) for x in line.split()]
        try:
            a[line[2]].append(line[1])
        except:
            a[line[2]] = [line[1]]
        try:
            b[line[3]].append(line[1])
        except:
            b[line[3]] = [line[1]]

with io.open('reciprocityIn.tab','wb') as f:
    for key in sorted(a.keys()):
        try:
            r = 1.*sum(a[key])/len(a[key])/key
        except:
            r = 0
        f.write(str(key)+"\t"+str(r)+"\t"+str(len(a[key]))+"\n")

with io.open('reciprocityOut.tab','wb') as f:
    for key in sorted(b.keys()):
        try:
            r = 1.*sum(b[key])/len(b[key])/key
        except:
            r = 0
        f.write(str(key)+"\t"+str(r)+"\t"+str(len(b[key]))+"\n")
