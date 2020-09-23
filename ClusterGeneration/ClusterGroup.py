from DistanceCalculation.Distance import *
import heapq


class ClusterGroup(object):
    """
    cluster_list: dict containing all clusters in the cluster group
    OG_matrix: distance matrix containing distance data on all individual elements
    cluster_matrix: distance matrix containing distance data between all clusters
    """
    def __init__(self, matrix, cluster_limit, cluster_list=None, PQ=None):
        if cluster_list is None:
            cluster_list = dict()

        self.__cluster_list = cluster_list
        self.__matrix = matrix
        self.__cluster_limit = cluster_limit
        self.__priority_queue = PQ

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

    def __str__(self):
        res = "Clusters:"
        clusters = self.get_all_clusters().values()
        for c in clusters:
            res += str(c)
        return res






