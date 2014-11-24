#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
import sys
import pymongo
import io
import numpy
import time
from datetime import datetime
from funcs import *

conn = pymongo.Connection()
db = conn.twitter
NODES = db.spammers

def getTop(ATTR,i=-1):
#    if ATTR == "location":
#        sortedKey= ["云南昆明","西藏","澳门","宁夏","青海","香港","海南","新疆","台湾","甘肃","贵州","海外","内蒙古","云南","吉林","山西","天津","重庆","黑龙江","江西","安徽","广西","辽宁","湖南","河北","陕西","四川","福建","上海","河南","湖北","山东","浙江","北京","江苏","其他","广东"]
#    elif ATTR =="date":
#        sortedKey = ["2009-08","2009-09","2009-10","2009-11","2009-12","2010-01","2010-02","2010-03","2010-04","2010-05","2010-06","2010-07","2010-08","2010-09","2010-10","2010-11","2010-12","2011-01","2011-02","2011-03","2011-04","2011-05","2011-06","2011-07","2011-08","2011-09","2011-10","2011-11","2011-12","2012-01"]
#    elif ATTR == "screen_name":
#        sortedKey = ["Tianyi_Account","Mobile_User","Others"]
#    else:
#        sortedKey = []
#
    clusters = getClusters('twitter')

    index = 0
    if i > -1:
        clusters = [clusters[i]]
    for cluster in clusters:
        cluster = {}.fromkeys(cluster)
        index += 1
        #if i > -1:
        #    print "cluster",i+1,
        #else:
        #    print "cluster",index
        spammers = {}
        with io.open('../twitterCrawler/nd.spammers') as f:
            count = 0
            for line in f:
                if count == i:
                    for spammer in line.split():
                        spammers[int(spammer)] = None
                    break
                count += 1
        infos = []
        for spammer in spammers:
            node = NODES.find_one({"id":spammer})
            if node == None:
                print 'spammer',spammer,'not found'
                sys.exit()
            if ATTR == "created_at":
                t = time.strptime(node['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                t = time.mktime(t)
                t = datetime.fromtimestamp(t).strftime("%Y-%m")
                infos.append(t)
            else:
                infos.append(node[ATTR])
        infos.sort()
        count = {}
        for info in infos:
            try:
                count[info]
            except:
                count[info] = 0
            count[info] += 1
        M = [(-1,None),(-1,None)]
        sortedKey = set(infos)
        if len(sortedKey) == 0:
            keys = count.keys()
        else:
            keys = sortedKey
        for key in keys:
            try:
                out = count[key]*1.0/len(infos)
            except KeyError:
                out = 0
            for m in M:
                if m[0] < out:
                    M.append((out,key))
                    break
            M.sort(key=lambda x:(x[0]))
            while len(M) > 2:
                M.pop(0)
        M.reverse()
        for i in M:
            print "&",i[1],"(","{:.2f}".format(i[0]*100),"\%)",
            #print ",",i[1],",","{:.2f}".format(i[0]*100),"%",
            break
 
if __name__ == "__main__":
    print sys.argv[1],
    for a in ["location","created_at","friends_count","followers_count","statuses_count"]:
        if len(sys.argv) > 0:
            print "\n",a,
            for i in sys.argv[1:]:
                getTop(a,int(i)-1)
        else:
            getTop(a)
    print "\\\\"
#    for i in sys.argv[1:]:
#        distinctTargets(int(i)-1)
