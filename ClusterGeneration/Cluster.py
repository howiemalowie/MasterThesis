class Cluster(object):

    def __init__(self, cluster_ID, elem_list=None, depot_elem=None, centroid=None,
                 children=None,  parent=None, solution=None):
        if elem_list is None:
            elem_list = []
        if depot_elem is None:
            depot_elem = 'D'
        self.__cluster_ID = cluster_ID
        self.__parent = parent
        self.__children = children
        self.__elem_list = elem_list
        self.__depot_elem = depot_elem
        self.__solution = solution
        self.__centroid = centroid

    def get_clusterID(self):
        return self.__cluster_ID

    def get_parent(self):
        return self.__parent

    def set_parent(self, ID):
        self.__parent = ID

    def get_children(self):
        return self.__children

    def set_children(self, IDList):
        self.__children = IDList

    def get_elements(self):
        return self.__elem_list

    def get_depot(self):
        return self.__depot_elem

    def get_cluster_size(self):
        return len(self.get_elements()) - 1

    def set_solution(self, solv):
        self.__solution = solv

    def get_solution(self):
        return self.__solution

    def set_centroid(self, centroid):
        self.__centroid = centroid

    def get_centroid(self):
        return self.__centroid

    def add_element(self, elem):
        self.__elem_list.append(elem)

    def remove_element(self, elem):
        self.__elem_list.remove(elem)

    def reset_cluster(self):
        self.__elem_list.clear()
        self.add_element(self.get_depot())
        self.add_element(self.get_centroid())

    def __str__(self):
        res = "\nCluster ID: " + str(self.get_clusterID())
        res += "\nDepot: " + str(self.get_depot())
        res += "\nCentroid: " + str(self.get_centroid())
        res += "\nTour: "
        for k in self.get_solution()[1]:
            res += str(k) + " "
        res += "\n"
        return res