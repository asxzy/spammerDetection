#!/usr/bin/env python
import sys,os
import ConfigParser

config = ConfigParser.RawConfigParser()

for dataset in ['weibo','twitter']:
    config.add_section(dataset)
    config.set(dataset,'name',dataset)
    config.set(dataset,'dir',sys.argv[1]+'/%(name)s')
    config.set(dataset,'graph','%(dir)s/%(name)s.graph')
    config.set(dataset,'seedList','%(dir)s/%(name)s.seedList')
    config.set(dataset,'seedDegree','%(dir)s/%(name)s.seedDegree')
    config.set(dataset,'nodeList','%(dir)s/%(name)s.nodeList')
    config.set(dataset,'nodeDegree','%(dir)s/%(name)s.nodeDegree')
    config.set(dataset,'top','30000')
    config.set(dataset,'threshold','0.9')
    config.set(dataset,'js','%(dir)s/%(name)s-%(top)s.js')
    config.set(dataset,'thresholdJS','%(dir)s/%(name)s-%(top)s-%(threshold)s.js')
    config.set(dataset,'spammers','%(dir)s/%(name)s-%(top)s-%(threshold)s.spammers')
    config.set(dataset,'spammerGraph','%(dir)s/%(name)s-%(top)s-%(threshold)s.spammerGraph')
    config.set(dataset,'nearDuplicates','%(dir)s/%(name)s-%(top)s-%(threshold)s.nearDuplicates')
    config.set(dataset,'nearDuplicatesJS','%(dir)s/%(name)s-%(top)s-%(threshold)s-nearDuplicates.js')
    config.set(dataset,'clusters','%(dir)s/%(name)s-%(top)s-%(threshold)s.clusters')
    config.set(dataset,'clusterSpammers','%(dir)s/%(name)s-%(top)s-%(threshold)s.clusterSpammers')
    config.set(dataset,'db','137.207.234.79')
    config.set(dataset,'dendrogram','%(dir)s/%(name)s-%(top)s-%(threshold)s.dendrogram')

with open('datasets.cfg','wb') as f:
    config.write(f)
