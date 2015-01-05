#!/usr/bin/env python 
import io,sys

with io.open(sys.argv[1]) as f:
    count = 0
    degree = []
    for line in f:
        line = line.split("\t")
        #degree.append([float(line[1]),float(line[2])])
        degree.append([float(line[11]),float(line[4])])
        count += 1
        if count == 6499:
            break
    count = 0
    for d in degree:
        if d[0]/d[1] > 0.9:
            count += 1
    print count

