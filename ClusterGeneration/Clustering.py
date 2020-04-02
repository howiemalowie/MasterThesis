#TODO: integrate distance matrix into cluster
class Cluster(object):

    def __init__(self, cluster_ID, elem_list=None, base_elem=None, total_dist=None):
        if elem_list is None:
            elem_list = []
        if base_elem is None:
            base_elem = 'B'
        if total_dist is None:
            total_dist = 0
        self.__cluster_ID = cluster_ID
        self.__elem_list = elem_list
        self.__base_elem = base_elem
        self.__total_dist = total_dist

    def get_clusterID(self):
        return self.__cluster_ID

    def get_elements(self):
        return self.__elem_list

    def get_base(self):
        return self.__base_elem

    def get_total_dist(self):
        return self.__total_dist

    def add_element(self, elem):
        self.__elem_list.append(elem)

    def remove_element(self, elem):
        self.__elem_list.remove(elem)
        # TODO: remove element by using main matrix

    def set_total_dist(self, matrix):
        total_dist = 0
        for e in self.__elem_dict.keys():
            for f in self.__elem_dict.keys():
                total_dist += (matrix[e][f] * matrix[f][e]) / 2
        self.__total_dist = total_dist

    def merge_clusters(self, c, matrix):
        for e in c.get_elements:
            self.__elem_list.append(e)

        self.set_total_dist(matrix)







