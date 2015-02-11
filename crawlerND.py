#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitter import *
import sys,io
from pprint import pprint
from random import randint

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
    IDS1 = Twitter("followers","/followers/ids")
    LISTS1= Twitter("followers","/followers/list")
    IDS2 = Twitter("friends","/friends/ids")
    LISTS2= Twitter("friends","/friends/list")
    URN = Twitter("users","/users/lookup")
    users = {}
    fgraph = io.open('topUsers.graph','wb')
    fusers = io.open('topUsers.json','wb')
    fseeds = io.open('topUsers.txt','wb')
    log = io.open('topUsers.log','wb')
    nds = {}
    with io.open(sys.argv[1]) as f:
        for line in f:
            nds[int(line)] = None
    spammers = {}
    for nd in nds:
        # followers
        followerList = []
        if IDS1.totalHit > LISTS1.totalHit:
            followerList,followerInfos = hitFollowersList(LISTS1,nd)
            for spammer in followerInfos:
                if spammer["id"] in spammers:
                    continue
                else:
                    spammers[spammer["id"]] = None
                fgraph.write(str(nd)+"\t"+str(spammer["id"])+"\n")
                fgraph.flush()
                fusers.write(json.dumps(spammer)+"\n")
                fusers.flush()
        else:
            followerList = hitFollowersIDs(IDS1,nd)
            userIdList = []
            for spammer in followerList:
                fgraph.write(str(nd)+"\t"+str(spammer)+"\n")
                fgraph.flush()
                if spammer in spammers:
                    continue
                else:
                    spammers[spammer] = None
                if len(userIdList) < 100:
                    userIdList.append(str(spammer))
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
        # friends
        friendList = []
        if IDS1.totalHit > LISTS1.totalHit:
            friendList,friendInfos = hitFriendsList(LISTS1,nd)
            for spammer in friendInfos:
                if spammer["id"] in spammers:
                    continue
                else:
                    spammers[spammer["id"]] = None
                fgraph.write(str(nd)+"\t"+str(spammer["id"])+"\n")
                fgraph.flush()
                fusers.write(json.dumps(spammer)+"\n")
                fusers.flush()
        else:
            friendList = hitFriendIDs(IDS1,nd)
            userIdList = []
            for spammer in friendList:
                fgraph.write(str(nd)+"\t"+str(spammer)+"\n")
                fgraph.flush()
                if spammer in spammers:
                    continue
                else:
                    spammers[spammer] = None
                if len(userIdList) < 100:
                    userIdList.append(str(spammer))
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


        log.write(str(nd)+"\n")
        log.flush()
    fgraph.close()
    fusers.close()
    log.close()
