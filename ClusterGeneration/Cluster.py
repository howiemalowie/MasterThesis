class Cluster(object):

    def __init__(self, cluster_ID, elem_list=None, base_elem=None, children=None,  parent=None):
        if elem_list is None:
            elem_list = []
        if base_elem is None:
            base_elem = 'B'
        self.__cluster_ID = cluster_ID
        self.__parent = parent
        self.__children = children
        self.__elem_list = elem_list
        self.__base_elem = base_elem

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