import heapq
from DistanceCalculation.Distance import *
from ClusterGeneration.Cluster import Cluster
from ClusterGeneration.ClusterGroup import ClusterGroup


def buildClusters(matrix, clusterLimit, depot, cf, include):
    clusterDict = dict()
    clusterID = 0
    for k in matrix.keys():
        if k != depot:
            elem_list = [depot, k]
            clusterDict[str(clusterID)] = Cluster(str(clusterID), elem_list, depot)
            clusterID += 1

    PQ = list()
    for c1ID in clusterDict.keys():
        for c2ID in clusterDict.keys():
            c1 = clusterDict[c1ID]
            c2 = clusterDict[c2ID]
            res = compute_cost_func(c1, c2, matrix, cf, include)
            PQ.append((res, c1ID, c2ID))

    heapq.heapify(PQ)
    clusterGroup = ClusterGroup(matrix, clusterLimit, clusterDict, PQ)
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


def compute_cost_func(c1, c2, link_mat, cf, include):
    a = c1.get_cluster_size()
    b = c2.get_cluster_size()
    if include:
        a += 1
        b += 1
    k = min(c1.get_cluster_size() // 5, c2.get_cluster_size() // 5)
    if k <= 0:
        k = 1
    if cf == "CLINK":
        return complete_linkage_clustering(c1, c2, link_mat, include)
    elif cf == "K-SLINK":
        return K_single_linkage_clustering(c1, c2, link_mat, k, include)
    else:
        return K_complete_linkage_clustering(c1, c2, link_mat, k, include)


def agglomerate(clusters, cf, include):
    cmpl_PQ = clusters.get_priority_queue()
    lmt = clusters.get_cluster_limit()
    cl = clusters.get_all_clusters()
    keys = cl.keys()
    merged = {k: False for k in keys}
    link_mat = clusters.get_matrix()

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
                    newDist = compute_cost_func(newCluster, c, link_mat, cf, include)
                    cmpl_PQ.append((newDist, cID, newID))
            heapq.heapify(cmpl_PQ)

            clusters.add_cluster(newCluster)
            merged[newID] = False
            merged[cID1] = True
            merged[cID2] = True
