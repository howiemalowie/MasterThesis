from DistanceCalculation.Distance import *
import heapq


class ClusterGroup(object):
    """
    cluster_list: dict containing all clusters in the cluster group
    OG_matrix: distance matrix containing distance data on all individual elements
    cluster_matrix: distance matrix containing distance data between all clusters
    """
    def __init__(self, matrix, cluster_limit, cluster_list=None):
        if cluster_list is None:
            cluster_list = dict()

        self.__cluster_list = cluster_list
        self.__matrix = matrix
        self.__cluster_limit = cluster_limit
        self.__priority_queue = self.calc_average_cluster_matrix()

    """
    Returns the dictionary object containing the clusters in the group
    """
    def get_all_clusters(self):
        return self.__cluster_list

    """ 
    Returns the maximum size of a cluster in the group
    """
    def get_cluster_limit(self):
        return self.__cluster_limit

    """ 
    Returns the cluster of given ID
    """
    def get_cluster(self, ID):
        return self.__cluster_list[ID]

    """
    Adds the given cluster to the cluster group
    """
    def add_cluster(self, cluster):
        self.__cluster_list[cluster.get_clusterID()] = cluster

    """
    Removes given cluster from the cluster group
    """
    def remove_cluster(self, ID):
        self.__cluster_list.pop(ID, None)


    """
    Returns the linkage matrix of all elements in the cluster group
    """
    def get_matrix(self):
        return self.__matrix

    """
    Returns the priority queue containing the order of cost function vale of
    all pair-wise unmerged clusters
    """
    def get_priority_queue(self):
        return self.__priority_queue

    def calc_average_cluster_matrix(self):
        PQ = list()
        clusters = self.get_all_clusters()
        limit = self.get_cluster_limit()
        matrix = self.get_matrix()
        for (c1ID, c1) in clusters.items():
            for (c2ID, c2) in clusters.items():
                if c1ID != c2ID and c1.get_cluster_size() + c2.get_cluster_size() <= limit:
                    res = complete_linkage_clustering(c1, c2, matrix)
                    PQ.append((res, c1ID, c2ID))

        heapq.heapify(PQ)
        return PQ

    def __str__(self):
        res = "Clusters:"
        clusters = self.get_all_clusters().values()
        for c in clusters:
            res += str(c)
        return res






