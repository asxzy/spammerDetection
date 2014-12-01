#!/usr/bin/env python
from funcs import *
from random import shuffle

spammers = getSpammersGroundTrue('twitter')
shuffle(spammers)
with io.open('randomSpammer.txt','wb') as f:
    count = 0
    for s in spammers:
        count += 1
        if count % 10000 == 0:
            print count
        f.write(str(s)+"\n")
