
class Graph(object):

    def __init__(self, graph_dict=None, coord_dict=None, depot_vertex=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be created
        """
        if graph_dict is None:
            graph_dict = {}
        if coord_dict is None:
            coord_dict = {}
        if depot_vertex is None:
            depot_vertex = 'D'
        self.__graph_dict = graph_dict
        self.__coord_dict = coord_dict
        self.__depot_vertex = depot_vertex

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        lst = list()
        for v in self.vertices():
            for edge in self.__graph_dict[v]:
                lst.append((v, edge, self.get_edgeweight(v, edge)))
        return lst

    def coords(self):
        """ returns the vertex info of a graph """
        return list(self.__coord_dict.values())

    def get_coord_dict(self):
        """ returns the dictionary of vertex info of a graph"""
        return self.__coord_dict

    def get_nodeweight(self, vertex):
        """ returns the weight of given vertex """
        [_, _, weight] = self.__coord_dict[vertex]
        return weight

    def set_nodeweight(self, vertex, weight):
        """ sets the weight of given node """
        [x, y, _] = self.__coord_dict[vertex]
        self.__coord_dict[vertex] = [x, y, weight]

    def get_edgeweight(self, v, u):
        """ returns the weight of given edge """
        edges = self.__graph_dict[v]
        return edges[u]

    def get_neighbors(self, vertex):
        """ returns neighbor set of given vertex """
        return self.__graph_dict[vertex].keys()

    def set_depot(self, vertex):
        """ sets the given vertex as the base vertex of the graph"""
        self.__depot_vertex = vertex

    def get_depot(self):
        """ returns the base vertex of the graph"""
        return self.__depot_vertex

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = dict()
        if vertex not in self.__coord_dict:
            self.__coord_dict[vertex] = []

    """ edge datatype:  {inGoing edge: edgeWeight}"""
    def add_edge(self, vertex1, vertex2, weight):
        """ assumes that edge is of type dict;
            between two vertices can be multiple edges!
        """
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1][vertex2] = weight
        else:
            self.add_vertex(vertex1)
            self.__graph_dict[vertex1] = {vertex2: weight}

    """ coord dataType: [X-coordinate, Y-coordinate, nodeWeight]"""
    def add_coords(self, vertex, coord):
        """ If the vertex is not in self.__graph_dict,
        a key "vertex" with an empty list as a value
        is added to both dicts. Otherwise just add coord to
        coord_dict
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = dict()
        if vertex not in self.__coord_dict:
            self.__coord_dict[vertex] = []
        self.__coord_dict[vertex] = coord

    def remove_vertex(self, vertex):
        # Remove all edges to vertex
        for v in self.vertices():
            self.__graph_dict[v].pop(vertex, None)

        # Remove vertex from graph
        if vertex in self.__graph_dict:
            del self.__graph_dict[vertex]
        if vertex in self.__coord_dict:
            del self.__coord_dict[vertex]

    def remove_edge(self, vertex, edge):
        # Removes the edge of given vertex
        if vertex in self.__graph_dict:
            if edge in self.edges():
                self.__graph_dict[vertex].remove(edge)

    def duplicate_vertex(self, vertex, dupes):
        if vertex in self.__graph_dict:
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            order = 0
            self.set_nodeweight(vertex, 1)
            nodeData = self.__coord_dict[vertex]
            edgeData = self.__graph_dict[vertex]
            new_vertices = list()
            while dupes > 1:
                # Naming convention: new vertex by adding a letter after ID, i.e. 1a
                myOrder = order
                new_vertex = str(vertex) + alphabet[myOrder % 26]
                while int(order / 26) > 0:
                    new_vertex += alphabet[myOrder % 26]
                    myOrder -= 26
                new_vertices.append(new_vertex)
                new_vertices.append(new_vertex)
                order += 1
                dupes -= 1

                # Add new vertex to graph with same data as original vertex
                self.add_vertex(new_vertex)
                self.add_coords(new_vertex, nodeData)
                for e in edgeData:
                    self.add_edge(new_vertex, e, edgeData[e])

                # Add edge to new vertex for all vertices with edge to original vertex
                vertices = self.vertices()
                for v in vertices:
                    if vertex in self.__graph_dict[v]:
                        self.add_edge(v, new_vertex, self.get_edgeweight(v, vertex))

            # Add edge between all duplicated nodes, with edgeweight 0
            for n in new_vertices:
                self.add_edge(vertex, n, 0.0)
                self.add_edge(n, vertex, 0.0)
                for m in new_vertices:
                    if m != n:
                        self.add_edge(n, m, 0.0)

    def __str__(self):
        res = "vertices: "
        for k in self.vertices():
            res += str(k) + " "
            res += str(self.__coord_dict[k]) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res



