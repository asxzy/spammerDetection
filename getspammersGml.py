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

for i in range(16):
    Graph = networkx.DiGraph()
    clusters = []
    clusters = getClusters('twitter')
    clusters = clusters[i]

    print i,clusters,
    spammers = getClusterSpammers('twitter')
    spammers = spammers[i]
    Allspammers = {}.fromkeys(spammers)

    shuffle(spammers)
    spammers = {}.fromkeys(spammers[:300])

    targets = {}

    '''Add near-dupliates'''
    '''Add spammers'''
    count = 0
    for spammer in spammers:
        for edge in EDGES.find({"from":spammer}):
            targets[edge["to"]] = None
            count += 1
            Graph.add_node(edge["from"],graphics="[fill \"#00ff00\"]")
            if edge["to"] in clusters:
                Graph.add_edge(edge["from"],edge["to"],fill="#ff0000")
            else:
                Graph.add_node(edge["to"],graphics="[fill \"#0000ff\"]")
                Graph.add_edge(edge["from"],edge["to"],fill="#0000ff")
    ##ND ff0000, spammer 00ff00, target 0000ff
    for cluster in clusters:
        Graph.add_node(cluster,graphics="[fill \"#ff0000\"]")
    for target in targets:
        if target in spammers:
            Graph.add_node(cluster,graphics="[fill \"#00ffff\"]")
        else:
            Graph.add_node(cluster,graphics="[fill \"#0000ff\"]")
    for spammer in spammers:
        Graph.add_node(edge["to"],graphics="[fill \"#00ff00\"]")

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
            
