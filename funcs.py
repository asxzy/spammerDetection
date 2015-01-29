#!/usr/bin/env python
import ConfigParser
import io
import pprint
import sys

c = ConfigParser.ConfigParser()
c.read('datasets.cfg')

def findJS(data):
    fout = io.open(c.get(data,'thresholdJS'),'wb')
    with io.open(c.get(data,'js')) as f:
        for line in f:
            if float(line.split()[2]) > float(c.get(data,'threshold')):
                fout.write(line)
    fout.close()

def findNearDuplicates(data):
    nds = {}
    with io.open(c.get(data,'thresholdJS')) as f:
        for line in f:
            line = line.split()
            nds[int(line[0])] = None
            nds[int(line[1])] = None

    print 'number of near duplicates:',len(nds)
    with io.open(c.get(data,'nearDuplicates'),'wb') as f:
        for n in sorted(nds.keys()):
            f.write(str(n))
            f.write('\n')
    print 'done' 

def getNearDuplicates(data):
    nds = []
    with io.open(c.get(data,'nearDuplicates')) as f:
        for line in f:
            nds.append(int(line))
    return nds

def findSeedList(data):
    nodes = {}
    with io.open(c.get(data,'graph')) as f:
        for line in f:
            line = [int(x) for x in line.split()]
            nodes[line[0]] = None
    with io.open(c.get(data,'seedList'),'wb') as f:
        for n in sorted(nodes.keys()):
            f.write(str(n))
            f.write('\n')

def getSeeds(data):
    nodes = []
    with io.open(c.get(data,'seedList')) as f:
        for line in f:
            nodes.append(int(line))
    return nodes 

def findSeedDegree(data):
    import pymongo
    conn = pymongo.Connection(c.get(data,'db'))
    db = conn.sina
    NODES = db.nodes

    degree = getNodeDegree(data)

    nodes = getSeeds(data)
    with io.open(c.get(data,'seedDegree'),'wb') as f:
        for n in nodes:
            node = NODES.find_one({'node_id':n})
            try:
                out = [node['node_id']]
            except TypeError:
                #print n,'not exsits'
                node = {}
                out = [n]
                node['friends_count'] = degree[n][0]
                node['followers_count'] = degree[n][1]
            try:
                out.append(node['friends_count'])
                out.append(node['followers_count'])
            except:
                out.append(node['out_degree'])
                out.append(node['in_degree'])
            f.write('\t'.join([str(x) for x in out])+'\n')

def findNodeList(data):
    nodes = {}
    with io.open(c.get(data,'graph')) as f:
        for line in f:
            line = [int(x) for x in line.split()]
            nodes[line[0]] = None
            nodes[line[1]] = None
    with io.open(c.get(data,'nodeList'),'wb') as f:
        for n in sorted(nodes.keys()):
            f.write(str(n))
            f.write('\n')

def getNodes(data):
    nodes = []
    with io.open(c.get(data,'nodeList')) as f:
        for line in f:
            nodes.append(int(line))
    return nodes 


def findNodeDegree(data):
    nodes = getNodes(data)
    Dnodes = {}.fromkeys(nodes)
    with io.open(c.get(data,'graph')) as f:
        for line in f:
            line = [int(x) for x in line.split()]
            try:
                Dnodes[line[0]][0] += 1
            except:
                Dnodes[line[0]] = [1,0]

            try:
                Dnodes[line[1]][1] += 1
            except:
                Dnodes[line[1]] = [0,1]

    with io.open(c.get(data,'nodeDegree'),'wb') as f:
        for n in nodes:
            f.write('\t'.join([str(x) for x in [n]+Dnodes[n]])+'\n')

def getNodeDegree(data):
    nodes = {}
    with io.open(c.get(data,'nodeDegree')) as f:
        for line in f:
            line = [int(x) for x in line.split()]
            nodes[line[0]] = (line[1],line[2])
    return nodes

def findSpammerGraph(data):
    spammers = {}.fromkeys(getNearDuplicates(data))
    fout = io.open(c.get(data,'spammerGraph'),'wb')
    with io.open(c.get(data,'graph')) as f:
        for line in f:
            line = line.split()
            if int(line[1]) in spammers:
                fout.write("\t".join(line)+"\n")

def findSpammers(data):
    spammers = {}
    nds = []
    with io.open(c.get(data,'thresholdJS')) as f:
        for line in f:
            line = line.split()
            nds.append({}.fromkeys([int(line[0]),int(line[1])]))
    count = 0
    for nd in nds:
        count += 1
        print 'doing nd',count,nd
        tmp_spammers = {}
        with io.open(c.get(data,'spammerGraph')) as f:
            for line in f:
                line = line.split()
                if int(line[1]) in nd:
                    try:
                        tmp_spammers[int(line[0])] += 1
                    except:
                        tmp_spammers[int(line[0])] = 1
        for spammer in tmp_spammers.keys():
            if tmp_spammers[spammer] == len(nd):
                spammers[spammer] = None
    print 'number of spammers:',len(spammers)
    with io.open(c.get(data,'spammers'),"wb") as f:
        for n in sorted([int(x) for x in spammers.keys()]):
            f.write(str(n))
            f.write('\n')
    print 'done'

def getSpammers(data):
    spammers = []
    with io.open(c.get(data,'spammers')) as f:
        for line in f:
            spammers.append(int(line))
    return spammers

def getSpammersGroundTrue(data):
    spammers = []
    with io.open(c.get(data,'spammers')+".groundTrue") as f:
        for line in f:
            spammers.append(int(line))
    return spammers


def findNearDuplicatesJS(data):
    Dnd = {}.fromkeys([int(x) for x in getNearDuplicates(data)])
    fout = io.open(c.get(data,'nearDuplicatesJS'),'w')
    with io.open(c.get(data,'js')) as f:
        for l in f:
            line = l.split()
            try:
                i = int(line[0])
                j = int(line[1])
            except:
                print line
                continue
                #sys.exit()
            if i in Dnd and j in Dnd:
                fout.write(l)
    fout.close()
 
def findCluster(data,color_threshold=None,showPlot=False):
    nds = getNearDuplicates(data)
    Dnd = {}
    for i,j in enumerate(nds):
        Dnd[j] = i

    matrix = [[0 for i in range(len(nds))] for j in range(len(nds))]

    with io.open(c.get(data,'nearDuplicatesJS')) as f:
        for line in f:
            line = line.split()
            i = int(line[0])
            j = int(line[1])
            matrix[Dnd[i]][Dnd[j]] = float(line[2])
            matrix[Dnd[j]][Dnd[i]] = float(line[2])
    for i in range(len(nds)):
        matrix[i][i] = "1"
    
    pdist = []
    for i in range(len(matrix)):
        for j in range(i+1,len(matrix)):
            pdist.append(1-matrix[i][j])
    import scipy.cluster.hierarchy
    #Z = scipy.cluster.hierarchy.linkage(pdist,method='average')
    Z = scipy.cluster.hierarchy.average(pdist)
    fout = io.open(c.get(data,'dendrogram'),'wb')
    for z in Z:
        z = z.tolist()
        z[0] = int(z[0]+1)
        z[1] = int(z[1]+1)
        z = [str(x) for x in z]
        fout.write("\t".join(z[:3])+"\n")
    fout.close()
    if showPlot:
        R = scipy.cluster.hierarchy.dendrogram(Z,color_threshold=color_threshold,show_leaf_counts=True)
        from matplotlib.pyplot import show
        show()

def findCluster(data,threshold):
    dendrogram = {}
    nds = getNearDuplicates(data)
    with io.open(c.get(data,'dendrogram')) as f:
        count = 0
        for line in f:
            count += 1
            line = line.split()
            if float(line[2]) > threshold:
                break
            dendrogram[count+len(nds)] = [int(line[0]),int(line[1])]
    count = 0
    flag = True
    while flag:
        count += 1
        flag = False
        keys = sorted(dendrogram.keys())
        keys.reverse()
        for key in keys:
            value = dendrogram[key]
            value.sort()
            value.reverse()
            for v in value:
                if v > len(nds):
                    tmp = value
                    del(tmp[tmp.index(v)])
                    dendrogram[v] += tmp
                    flag = True
                    break
            if flag:
                del(dendrogram[key])
                break

    clusters = []
    for key in dendrogram:
        clusters.append(dendrogram[key])
    clusters.sort(key=lambda x : len(x))
    with io.open(c.get(data,'clusters'),'wb') as f:
        for cluster in clusters:
            f.write("\t".join([str(nds[x-1]) for x in cluster])+"\n")

def getClusters(data):
    clusters = []
    with io.open(c.get(data,'clusters')) as f:
        for line in f:
            clusters.append([int(x) for x in line.split()])
    return clusters



def findClusterSpammers(data):
    clusters = getClusters(data)
    fout = io.open(c.get(data,'clusterSpammers'),"wb")
    spammers = {}.fromkeys(getSpammers(data))
    count = 0
    for cluster in clusters:
        out = []
        count += 1
        print 'doing cluster',count
        nds = {}.fromkeys(cluster)
        with io.open(c.get(data,'spammerGraph')) as f:
            for line in f:
                line = line.split()
                if int(line[1]) in cluster and int(line[0]) in spammers:
                    out.append(int(line[0]))
        out.sort()
        fout.write("\t".join([str(x) for x in out])+"\n")
    fout.close()
    print 'done'

def getClusterSpammers(data):
    cluster = []
    with io.open(c.get(data,'clusterSpammers')) as f:
        for line in f:
            cluster.append([int(x) for x in line.split()])
    return cluster

def getClusterSpammersGroundTrue(data):
    cluster = []
    with io.open(c.get(data,'clusterSpammers')+".groundTrue") as f:
        for line in f:
            cluster.append([int(x) for x in line.split()])
    return cluster
