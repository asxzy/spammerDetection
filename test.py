import io,sys
a = []
with io.open('cluster_infos.out') as f:
    for line in f:
        line = line.split('&')
        a.append(line)
a.sort(key = lambda x:float(x[1]))
for cluster in a:
    print "&".join(cluster),

a = []
with io.open('verifyCluster.log') as f:
    for line in f:
        line = line.replace("\n","")
        line = line.split('&')
        a.append(line)
for i in range(17):
    print i,
    for cluster in a:
        print "&",cluster[i],
    print "\\\\\n",
