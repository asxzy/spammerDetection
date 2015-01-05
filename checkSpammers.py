#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

import sys,io
sys.path.append('/Volumes/Data/asxzy/github/twitterCrawler')
import pymongo
from twitter import *
from random import randint,shuffle
from funcs import *


def run():
    NODES = pymongo.Connection().twitter.spammers
    Worker = Twitter("search","/search/tweets")

    log = io.open('checkSpammers.log','ab')
    spammers = getSpammersGroundTrue('twitter')
    shuffle(spammers)
    count = 0
    count2 = 0
    for spammer in spammers:
        node = NODES.find_one({"id":spammer})
        res = Worker.checkSpammer(node["screen_name"])
        if res:
            count += 1
        else:
            count2 += 1
        print count,count2


    log.close()

if __name__ == '__main__':
    run()
