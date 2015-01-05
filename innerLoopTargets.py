#!/usr/bin/env pypy
import io
import sys

infos = {}
with io.open('innerLoopTargets.log') as f:
    for line in f:
        line = line.split()
        try:
            infos[int(line[0])]
        except:
            infos[int(line[0])] = []
        infos[int(line[0])].append((line[2],line[4]))
for info in sorted(infos.keys()):
    loop = 0
    inDeg = 0
    for a in infos[info]:
        loop += int(a[0])
        inDeg += int(a[1])
    print info,loop,inDeg,1.0*loop/inDeg

