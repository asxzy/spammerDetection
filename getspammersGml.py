#!/usr/bin/env pypy
import io,sys
import math
import pymongo
from random import shuffle
from funcs import *
import networkx



conn = pymongo.Connection()
db = conn.twitter
NODES = db.nodes
EDGES = db.graph

for i in range(10,16):
    Graph = networkx.DiGraph()
    clusters = []
    clusters = getClusters('twitter')
    cluster = clusters[i]

    print i,cluster,
    spammers = getClusterSpammers('twitter')
    spammers = spammers[i]

    shuffle(spammers)
    spammers = spammers[:300]
    '''Add near-dupliates'''
    '''Add spammers'''
    count = 0
    for spammer in spammers:
        for edge in EDGES.find({"from":spammer}):
            count += 1
            Graph.add_node(edge["from"],graphics="[fill \"#00ff00\"]")
            if edge["to"] in cluster:
                Graph.add_node(edge["to"],graphics="[fill \"#ff0000\"]")
                Graph.add_edge(edge["from"],edge["to"],fill="#ff0000")
            else:
                Graph.add_node(edge["to"],graphics="[fill \"#0000ff\"]")
                Graph.add_edge(edge["from"],edge["to"],fill="#0000ff")
    print len(spammers),count
    filename = "/Volumes/Data/asxzy/datasets/spammer/twitter/cluster/cluster_"+"%02d"%(i+1)+".gml"
    print filename
    gml = networkx.generate_gml(Graph)
    count = 0
    with open(filename, "wb") as fout:
        for line in gml:
            line = line.replace("\"[fill","[fill")
            line = line.replace("]\"","]")
            line += "\n"
            fout.write(line)
            
