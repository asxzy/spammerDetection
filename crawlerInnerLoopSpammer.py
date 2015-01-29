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

log = io.open('innerLoopSpammer.log','wb')
clusters = getClusterSpammers('twitter')
spammers = {}.fromkeys(getSpammersGroundTrue('twitter'))
for i,users in enumerate(clusters):
    #if i < 7:
    #    continue
    count = 0
    shuffle(users)
    for user in users[:100]:
        userInfo = hitUser(URN,user)
        try:
            if userInfo["protected"]:
                continue
        except:
            continue
        InLinks = 0
        OutLinks = 0
        targets = {}
        # s => t
        friendList = hitFriendsIDs(IDS1,user)
        for friend in friendList:
            if friend in spammers:
                OutLinks += 1
        # s <= t
        followerList = hitFollowersIDs(IDS2,user)
        for follower in followerList:
            if follower in spammers:
                InLinks += 1
        print i,user,InLinks,OutLinks,userInfo["followers_count"],userInfo["friends_count"]
        log.write(str(i)+"\t")
        #log.write(str(user)+"\t")
        log.write("InLinks\t"+str(InLinks)+"\t")
        log.write("OutLinks\t"+str(OutLinks)+"\t")
        log.write("followers_count\t"+str(userInfo["followers_count"])+"\t")
        log.write("friends_count\t"+str(userInfo["friends_count"])+"\n")
        log.flush()
log.close()
