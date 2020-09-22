import heapq
from DistanceCalculation.Distance import *
from ClusterGeneration.Cluster import Cluster
from ClusterGeneration.ClusterGroup import ClusterGroup


def buildClusters(matrix, clusterLimit, depot):
    clusterList = dict()
    clusterID = 0
    for k in matrix.keys():
        if k != depot:
            elem_list = [depot, k]
            clusterList[str(clusterID)] = Cluster(str(clusterID), elem_list, depot)
            clusterID += 1
    clusterGroup = ClusterGroup(matrix, clusterLimit, clusterList)
    return clusterGroup


def merge_clusters(cluster1, cluster2):
    ID1 = cluster1.get_clusterID()
    ID2 = cluster2.get_clusterID()
    ele1 = cluster1.get_elements()
    ele2 = cluster2.get_elements()
    newList = ele1 + list(set(ele2) - set(ele1))
    newID = ID1 + ", " + ID2
    depot = cluster1.get_depot()
    children = [ID1, ID2]
    newCluster = Cluster(newID, newList, depot, None, children)
    cluster1.set_parent(newID)
    cluster2.set_parent(newID)

    return newCluster


def agglomerate(clusters):
    cmpl_PQ = clusters.get_priority_queue()
    lmt = clusters.get_cluster_limit()
    cl = clusters.get_all_clusters()
    keys = cl.keys()
    merged = {k: False for k in keys}

    while cmpl_PQ:
        (dist, cID1, cID2) = heapq.heappop(cmpl_PQ)

        if not merged[cID1] and not merged[cID2]:
            cluster1 = clusters.get_cluster(cID1)
            cluster2 = clusters.get_cluster(cID2)
            newCluster = merge_clusters(cluster1, cluster2)
            newID = newCluster.get_clusterID()

            # Update matrix and rebuild heap
            for cID, c in cl.items():
                if newCluster.get_cluster_size() + c.get_cluster_size() <= lmt\
                        and not merged[cID]:
                    newDist = complete_linkage_clustering(newCluster, c, clusters.get_matrix())
                    cmpl_PQ.append(newDist, cID, newID)
            heapq.heapify(cmpl_PQ)

            clusters.add_cluster(newCluster)
            merged[newID] = False
            merged[cID1] = True
            merged[cID2] = True
