class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return list(self.__graph_dict.values())

    def add_vertex(self, vertex, lon, lat):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[(vertex, lon, lat)] = []

    def add_edge(self, vertex, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        if vertex in self.__graph_dict:
            self.__graph_dict[vertex].append(edge)
        else:
            self.add_vertex(vertex)
            self.__graph_dict[vertex].append(edge)

    def __str__(self):
        res = "vertices: "
        for k in self.vertices():
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res



[vertices, edges] = list(map(int, input()))

for i in range(vertices)


