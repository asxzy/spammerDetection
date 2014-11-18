#!/usr/bin/env python
from funcs import *
import sys,io
sys.path.append('../twitterCrawler')
from twitter import *


if __name__ == '__main__':

    twitter = Twitter("users","/users/show/:id")
    data = 'twitter'
    ND = getNearDuplicates(data)
    fout = io.open(c.get(data,'nearDuplicates')+"-screen_name",'wb')
    for nd in ND:
        print nd
        fout.write(twitter.getUser(int(nd))["screen_name"]+"\n")
        fout.flush()
    fout.close()
