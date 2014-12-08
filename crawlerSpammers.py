#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io
sys.path.append('/Volumes/Data/asxzy/github/spammerDetection/twitterCrawler')
from twitter import *
from pprint import pprint
from random import randint
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


if __name__ == '__main__':
    i = 4
    IDS = Twitter("followers","/followers/ids")
    LISTS= Twitter("followers","/followers/list")
    URN = Twitter("users","/users/lookup")
    users = {}
    fgraph = io.open('spammerCluster'+str(i)+'.graph','wb')
    fusers = io.open('spammerCluster'+str(i)+'.json','wb')
    fseeds = io.open('spammerCluster'+str(i)+'.txt','wb')
    log = io.open('spammerCluster'+str(i)+'.log','wb')
    spammers = {}.fromkeys(getClusterSpammersGroundTrue('twitter')[i-1])
    for spammer in spammers:
        followerList = hitFriendsIDs(IDS,spammer)
        userIdList = []
        for follower in followerList:
            fgraph.write(str(spammer)+"\t"+str(follower)+"\n")
            fgraph.flush()
            if len(userIdList) < 100:
                userIdList.append(str(follower))
                continue
            userList = hitUser(URN,userIdList)
            for u in userList:
                fusers.write(json.dumps(u)+"\n")
                fusers.flush()
            userIdList = []
        if len(userIdList) > 0:
            userList = hitUser(URN,userIdList)
            for u in userList:
                fusers.write(json.dumps(u)+"\n")
                fusers.flush()
        log.write(str(spammer)+"\n")
        log.flush()
    fgraph.close()
    fusers.close()
    log.close()
