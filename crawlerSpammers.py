#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io
sys.path.append('/Volumes/Data/asxzy/github/twitterCrawler')
import pymongo
from twitter import *
from random import randint,shuffle
from funcs import *

userHitCount = 0

def hitFollowersIDs(worker,uid):
    flist = []
    try:
        flist = worker.getFollowerIDs(uid)
    except Exception, e:
        print e
    return flist

def hitFollowersList(worker,uid):
    flist = []
    finfos = []
    try:
        flist,finfos = worker.getFollowerList(uid)
    except Exception, e:
        print e
    return flist,finfos


def hitFriendsIDs(worker,uid):
    flist = []
    try:
        flist = worker.getFriendIDs(uid)
    except Exception, e:
        print e
    return flist

def hitFriendsList(worker,uid):
    flist = []
    finfos = []
    try:
        flist,finfos = worker.getFriendList(uid)
    except Exception, e:
        print e
    return flist,finfos

def hitUser(worker,userIdList):
    global userHitCount
    users = []
    try:
        users = worker.getUserList(userIdList)
        userHitCount += len(userIdList)
    except Exception, e:
        print e
    return users

IDS1 = Twitter("friends","/friends/ids")
LISTS1 = Twitter("friends","/friends/list")

IDS2 = Twitter("followers","/followers/ids")
LISTS2 = Twitter("followers","/followers/list")

URN = Twitter("users","/users/lookup")
SPAMMERS = {}.fromkeys(getSpammersGroundTrue('twitter'))

def run(i):
    log = io.open('innerLoopTargets.log','ab')
    spammers = getClusterSpammersGroundTrue('twitter')[i]
    NODES = pymongo.Connection().twitter.spammers
    shuffle(spammers)
    Aspammers = {}.fromkeys(spammers)
    sFollowers = {}
    count = 0
    for spammer in spammers[:1000]:
        InLinks = 0
        inDeg = 0
        targets = {}
        node = NODES.find_one({"id":spammer})
        # s => t
        if node["friends_count"] > 200:
            friendList = hitFriendsIDs(IDS1,spammers)
        else:
            friendList,friendInfos = hitFriendsList(LISTS1,spammer)
        for friend in friendList:
            targets[friend] = None
        # s <= t
        if node["followers_count"] > 200:
            followerList = hitFollowersIDs(IDS1,spammers)
        else:
            followerList,followerInfos = hitFollowersList(LISTS1,spammer)
        for follower in followerList:
            inDeg += 1
            if follower in targets:
                InLinks += 1
        print i,InLinks,inDeg,len(targets)
        log.write(str(i+1)+"\t")
        log.write("InLinks\t"+str(InLinks)+"\t")
        log.write("InDegree\t"+str(inDeg)+"\t")
        log.write("targets\t"+str(len(targets))+"\n")
        log.flush()
    log.close()

if __name__ == '__main__':
    for i in range(16):
        run(i)
