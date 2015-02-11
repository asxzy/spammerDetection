#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io
sys.path.append('/Volumes/Data/asxzy/github/twitterCrawler')
from twitter import *
from random import randint,shuffle
from funcs import *
from sets import Set
import simplejson as json

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

log = io.open('reciprocity.log','wb')
#graph = io.open('reciprocity.graph','wb')
#raw = io.open('reciprocity.json','wb')
log.write('id\treciprocity\tfollowers_couint\tfriends_count\n')
users = []
while len(users) < 1000000:
    userIdList = []
    while len(userIdList) < 100:
        uid = randint(0, 3000000000)
        if uid not in users:
            userIdList.append(str(uid))
    userList = hitUserList(URN,userIdList)
    for user in userList:
        #raw.write(json.dumps(user)+"\n")
        if user["protected"] or user['followers_count'] == 0 or user['friends_count'] == 0:
            continue
        users.append(user)
        friendList = hitFriendsIDs(IDS1,user['id'])
        followerList = hitFollowersIDs(IDS2,user['id'])
        reciprocity = len(Set(friendList) & Set(followerList))
        print user['id'],reciprocity,len(friendList),len(followerList)
        log.write(str(user['id'])+"\t")
        log.write(str(reciprocity)+"\t")
        log.write(str(len(friendList))+"\t")
        log.write(str(len(followerList))+"\n")
        log.flush()
log.close()
