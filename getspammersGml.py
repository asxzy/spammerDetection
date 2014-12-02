#!/usr/bin/env pypy
import io,sys
import math
import pymongo
from random import shuffle
import networkx

Graph = networkx.DiGraph()


conn = pymongo.Connection()
db = conn.sina
NODES = db.nodes
EDGES = db.edges

print sys.argv[1]
clusters = []
with io.open('/Users/asxzy/datasets/weibo.395.cluster') as f:
    for line in f:
        clusters.append([int(x) for x in line.split()])

cluster = clusters[int(sys.argv[1])-1]
spammers = {}

for edge in EDGES.find({"to":{"$in":cluster}}):
    spammers[edge["from"]] = True
spammers = spammers.keys()
shuffle(spammers)
spammers = spammers[:300]
'''Add near-dupliates'''
'''Add spammers'''
for spammer in spammers:
    try:
        NODES.find_one({"node_id":spammer})["SpammerIndex"]
        for edge in EDGES.find({"from":spammer}):
            Graph.add_node(edge["from"],graphics="[fill \"#00ff00\"]")
            if edge["to"] in cluster:
                Graph.add_node(edge["to"],graphics="[fill \"#ff0000\"]")
                Graph.add_edge(edge["from"],edge["to"],fill="#ff0000")
            else:
                Graph.add_node(edge["to"],graphics="[fill \"#0000ff\"]")
                Graph.add_edge(edge["from"],edge["to"],fill="#0000ff")
    except KeyError:
        continue
filename = "/Users/asxzy/datasets/cluster/cluster_"+"%02d"%int(sys.argv[1])+".gml"
gml = networkx.generate_gml(Graph)
count = 0
with open(filename, "wb") as fout:
    for line in gml:
        line = line.replace("\"[fill","[fill")
        line = line.replace("]\"","]")
        line += "\n"
        fout.write(line)
        
