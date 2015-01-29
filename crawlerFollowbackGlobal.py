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

def hitUser(worker,user):
    try:
        user = worker.getUser(user)
    except Exception, e:
        print e
    return user


def hitUserList(worker,userIdList):
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

URN = Twitter("users","/users/show/:id")

log = io.open('innerLoopGlobal.log','ab')
users = []
#with io.open('/Volumes/Data/asxzy/datasets/spammer/twitter/twitter.topOut20000') as f:
with io.open('/Volumes/Data/asxzy/datasets/spammer/twitter/twitter.randomNodes') as f:
    for line in f:
        users.append(int(line.split()[0]))
#shuffle(users)
count = 0
for user in users[:10000]:
    userInfo = hitUser(URN,user)
    if userInfo["protected"]:
        continue
    InLinks = 0
    inDeg = 0
    targets = {}
    # s => t
    friendList = hitFriendsIDs(IDS1,user)
    for friend in friendList:
        targets[friend] = None
    # s <= t
    followerList = hitFollowersIDs(IDS2,user)
    for follower in followerList:
        inDeg += 1
        if follower in targets:
            InLinks += 1
    print user,InLinks,inDeg,len(targets),userInfo["followers_count"],userInfo["friends_count"]
    log.write(str(user)+"\t")
    log.write("InLinks\t"+str(InLinks)+"\t")
    log.write("followers_count\t"+str(userInfo["followers_count"])+"\t")
    log.write("friends_count\t"+str(userInfo["friends_count"])+"\n")
    log.flush()
log.close()
