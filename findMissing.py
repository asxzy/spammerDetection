#!/usr/bin/env pypy
import io,sys

users = {}
with io.open(sys.argv[1]) as f:
    for line in f:
        users[int(line)] = None

fout = io.open('missingSeed.txt','wb')
with io.open(sys.argv[2]) as f:
    for line in f:
        if int(line.split()[0]) in users:
            fout.write(line)
fout.close()
