#!/usr/bin/env pypy
import io
import sys

with io.open('innerLoop.log') as f:
    count = 0
    i = 0
    j = 0
    for line in f:
        line = line.split()
        if count % 7 == 0:
            print line[0],"&",
        elif count % 7 == 1:
            i = int(line[1])
        elif count % 7 == 2:
            j = int(line[1])
        elif count % 7 == 3:
            print "{:.3f}".format(i/float(line[1])*100),'\% &',"{:.3f}".format(j/float(line[1])*100),'\% &',
        elif count % 7 == 4:
            i = int(line[1])
        elif count % 7 == 5:
            j = int(line[1])
        elif count % 7 == 6:
            print "{:.3f}".format(i/float(line[1])*100),'\% &',"{:.3f}".format(j/float(line[1])*100),'\% \\\\'

        count += 1
