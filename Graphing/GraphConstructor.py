from Graphing.ConnectGraph import connectGraph
from Graphing.GeneratePOI import generatePOI


class Graph(object):

    def __init__(self, graph_dict=None, coord_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict is None:
            graph_dict = {}
        if coord_dict is None:
            coord_dict = {}
        self.__graph_dict = graph_dict
        self.__coord_dict = coord_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return list(self.__graph_dict.values())

    def coords(self):
        return list(self.__coord_dict.values())

    def get_nodeweight(self, vertex):
        [_, _, weight] = self.__coord_dict[vertex]
        return weight

    def set_nodeweight(self, vertex, weight):
        [x, y, _] = self.__coord_dict[vertex]
        self.__coord_dict[vertex] = [x, y, weight]

    # NEED TO OPTIMIZE THIS
    def get_edgeweight(self, v, u):
        edges = self.__graph_dict[v]
        for e in edges:
            if e[1] == u:
                return e[2]
        return -1

    def get_neighbors(self, vertex):
        neighbors = list()
        for edge in self.__graph_dict[vertex]:
            neighbors.append(edge[1])
        return neighbors

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
        if vertex not in self.__coord_dict:
            self.__coord_dict[vertex] = []

    def add_edge(self, vertex, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        if vertex in self.__graph_dict:
            self.__graph_dict[vertex].append(edge)
        else:
            self.add_vertex(vertex)
            self.__graph_dict[vertex].append(edge)

    def add_coords(self, vertex, coord):
        """ If the vertex is not in self.__graph_dict,
        a key "vertex" with an empty list as a value
        is added to both dicts. Otherwise just add coord to
        coord_dict
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
        if vertex not in self.__coord_dict:
            self.__coord_dict[vertex] = []
        self.__coord_dict[vertex] = coord

    def remove_vertex(self, vertex):
        if vertex in self.__graph_dict:
            del self.__graph_dict[vertex]
        if vertex in self.__coord_dict:
            del self.__coord_dict[vertex]

    def remove_edge(self, vertex, edge):
        if vertex in self.__graph_dict:
            self.__graph_dict[vertex].remove(edge)


    def __str__(self):
        res = "vertices: "
        for k in self.vertices():
            res += str(k) + " "
            res += str(self.__coord_dict[k]) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res



