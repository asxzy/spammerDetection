#!/usr/bin/env pypy
# -*- coding: utf-8 -*- 
import io
import pymongo
from funcs import *

conn = pymongo.Connection("localhost")
db = conn.twitter
NODES = db.nodes
EDGES = db.graph


zbs = getSpammers('twitter')
print type(zbs),len(zbs)

count = 0
EDGES.update({"from":{"$in":zbs}},{"$set":{"spammed":True}},multi=True)
EDGES.ensure_index("spammed")
