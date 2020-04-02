from ClusterGeneration.Clustering import Cluster


def complete_linkage_clustering(cluster1, cluster2, matrix):
    #TODO: implement complete
    elems1 = cluster1.get_elements()
    elems2 = cluster2.get_elements()
    max_dist = 0
    for e1 in elems1:
        for e2 in elems2:
            new_dist = (matrix[e1][e2] + matrix[e2][e1]) / 2
            max_dist = max(max_dist, new_dist)
    return max_dist


def single_linkage_clustering(cluster1, cluster2, matrix):
    #TODO: implement single
    elems1 = cluster1.get_elements()
    elems2 = cluster2.get_elements()
    min_dist = float("Inf")
    for e1 in elems1:
        for e2 in elems2:
            new_dist = (matrix[e1][e2] + matrix[e2][e1]) / 2
            min_dist = min(min_dist, new_dist)
    return min_dist


def avg_linkage_clustering(cluster1, cluster2, matrix):
    #TODO: implement average
    elems1 = cluster1.get_elements()
    elems2 = cluster2.get_elements()
    cluster_size = len(elems1) + len(elems2)
    sum_dist = 0
    for e1 in elems1:
        for e2 in elems2:
            sum_dist += (matrix[e1][e2] + matrix[e2][e1]) / 2
    return sum_dist / cluster_size
