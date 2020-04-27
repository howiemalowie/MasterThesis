from Graphing.graphTesting import main_test
from ClusterGeneration.Clustering import *
import heapq


def agglomerate(clusters):
    avg_PQ = clusters.get_priority_queue()
    merged = dict()

    while avg_PQ:
        (dist, cID1, cID2) = heapq.heappop(avg_PQ)
        if cID1 not in merged and cID2 not in merged:
            cluster1 = clusters.get_cluster(cID1)
            cluster2 = clusters.get_cluster(cID2)
            clusters.merge_clusters(cluster1, cluster2)
            merged[cID1] = True
            merged[cID2] = True


def buildClusters(matrix, clusterLimit, base):
    clusterList = dict()
    clusterID = 0
    for k in matrix.keys():
        if k != base:
            elem_list = [base, k]
            clusterList[str(clusterID)] = Cluster(str(clusterID), elem_list, base)
            clusterID += 1
    clusterGroup = ClusterGroup(matrix, clusterLimit, clusterList)
    return clusterGroup


if __name__ == "__main__":
    matrix, clusterLimit, b = main_test()

    Clusters = buildClusters(matrix, clusterLimit, b)

    print(Clusters)
    print("merging clusters:")
    agglomerate(Clusters)
    print(Clusters)
