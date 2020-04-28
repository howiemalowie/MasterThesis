import heapq
from DistanceCalculation.Distance import *


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
        self.__OG_matrix = matrix
        self.__cluster_limit = cluster_limit
        self.__priority_queue = self.calc_average_cluster_matrix()

    def get_all_clusters(self):
        return self.__cluster_list

    def get_cluster_limit(self):
        return self.__cluster_limit

    def add_cluster(self, cluster):
        self.__cluster_list[cluster.get_clusterID()] = cluster

    def get_cluster(self, ID):
        return self.__cluster_list[ID]

    def remove_cluster(self, ID):
        self.__cluster_list.pop(ID, None)

    def get_OG_matrix(self):
        return self.__OG_matrix

    def get_priority_queue(self):
        return self.__priority_queue

    def calc_average_cluster_matrix(self):
        PQ = list()
        clusters = self.get_all_clusters()
        limit = self.get_cluster_limit()
        for (c1ID, c1) in clusters.items():
            for (c2ID, c2) in clusters.items():
                if c1ID != c2ID and c1.get_cluster_size() + c2.get_cluster_size() <= limit:
                    res = avg_linkage_clustering(c1, c2, self.get_OG_matrix())
                    heapq.heappush(PQ, (res, c1ID, c2ID))
        return PQ

    def merge_clusters(self, cluster1, cluster2):
        clusterID1 = cluster1.get_clusterID()
        clusterID2 = cluster2.get_clusterID()
        clusters = self.get_all_clusters()
        newCluster = self.get_merged_clusters(cluster1, cluster2)
        newID = newCluster.get_clusterID()

        self.remove_cluster(clusterID1)
        self.remove_cluster(clusterID2)

        # Update matrix
        for cID, c in clusters.items():
            if newCluster.get_cluster_size() + c.get_cluster_size() <= self.__cluster_limit:
                newDist = avg_linkage_clustering(newCluster, c, self.get_OG_matrix())
                heapq.heappush(self.__priority_queue, (newDist, cID, newID))

        self.add_cluster(newCluster)

    @staticmethod
    def get_merged_clusters(c1, c2):
        ID1 = c1.get_clusterID()
        ID2 = c2.get_clusterID()
        ele1 = c1.get_elements()
        ele2 = c2.get_elements()
        newList = ele1 + list(set(ele2) - set(ele1))
        newID = ID1 + ", " + ID2
        newCluster = Cluster(newID, newList)
        return newCluster

    def __str__(self):
        res = "Clusters:"
        clusters = self.get_all_clusters().values()
        for c in clusters:
            res += str(c)
        return res


class Cluster(object):

    def __init__(self, cluster_ID, elem_list=None, base_elem=None):
        if elem_list is None:
            elem_list = []
        if base_elem is None:
            base_elem = 'B'
        self.__cluster_ID = cluster_ID
        self.__elem_list = elem_list
        self.__base_elem = base_elem

    def get_clusterID(self):
        return self.__cluster_ID

    def get_elements(self):
        return self.__elem_list

    def get_base(self):
        return self.__base_elem

    def get_cluster_size(self):
        return len(self.get_elements()) - 1

    def add_element(self, elem):
        self.__elem_list.append(elem)

    def remove_element(self, elem):
        self.__elem_list.remove(elem)

    def __str__(self):
        res = "\nCluster ID: " + str(self.get_clusterID())
        res += "\nNodes: "
        for k in self.get_elements():
            res += str(k) + " "
        res += "\n"
        return res



