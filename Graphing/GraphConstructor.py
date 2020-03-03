
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
        lst = list()
        for edges in self.__graph_dict.values():
            for e in edges:
                lst.append(e)
        return lst

    def coords(self):
        """ returns the vertex info of a graph """
        return list(self.__coord_dict.values())

    def get_nodeweight(self, vertex):
        """ returns the weight of given vertex """
        [_, _, weight] = self.__coord_dict[vertex]
        return weight

    def set_nodeweight(self, vertex, weight):
        """ sets the weight of given node """
        [x, y, _] = self.__coord_dict[vertex]
        self.__coord_dict[vertex] = [x, y, weight]

    # NEED TO OPTIMIZE THIS (O(m) runtime)
    def get_edgeweight(self, v, u):
        """ returns the weight of given edge """
        edges = self.__graph_dict[v]
        for e in edges:
            if e[1] == u:
                return e[2]
        return -1

    def get_neighbors(self, vertex):
        """ returns neighbor set of given vertex """
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

    """ edge datatype:  [outgoing vertex, inbound vertex, weight]"""
    def add_edge(self, vertex, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        if vertex in self.__graph_dict:
            self.__graph_dict[vertex].append(edge)
        else:
            self.add_vertex(vertex)
            self.__graph_dict[vertex].append(edge)

    """ coord dataType: [X-coordinate, Y-coordinate, nodeWeight]"""
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

    # NEED TO OPTIMIZE (O(n) runtime when contracting)
    def remove_vertex(self, vertex, contract=False):
        if contract:
            edges = self.__graph_dict[vertex]
            outV = list()
            inV = list()
            lengthout = list()
            lengthin = list()
            for e in edges:
                inV.append(e[1])
                lengthin.append(e[2])

            edges = self.edges()
            for e in edges:
                if e[1] == vertex:
                    outV.append(e[0])
                    self.remove_edge(e[0], e)
                    lengthout.append(e[2])

            for o in range(len(outV)):
                for i in range(len(inV)):
                    self.add_edge(outV[o], [outV[o], inV[i], lengthin[i] + lengthout[o]])

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
            newVertices = list()
            while dupes > 1:
                # Naming convention: new vertex by adding a letter after ID, i.e. 1a
                myOrder = order
                newVertex = str(vertex) + alphabet[myOrder % 26]
                while int(order / 26) > 0:
                    newVertex += alphabet[myOrder % 26]
                    myOrder -= 26
                newVertices.append(newVertex)
                order += 1
                dupes -= 1

                # Add new vertex to graph with same data as original vertex
                self.add_vertex(newVertex)
                self.add_coords(newVertex, nodeData)
                for [outV, inV, w] in edgeData:
                    self.add_edge(newVertex, [newVertex, inV, w])

                # Add edge to new vertex for all vertices with edge to original vertex
                edges = self.edges()
                for [outV, inV, w] in edges:
                    if inV == vertex:
                        self.add_edge(outV, [outV, newVertex, w])

            # Add edge between all duplicated nodes, with edgeweight 0
            for n in newVertices:
                self.add_edge(vertex, [vertex, n, 0.0])
                self.add_edge(n, [n, vertex, 0.0])
                for m in newVertices:
                    if m != n:
                        self.add_edge(n, [n, m, 0.0])

    def __str__(self):
        res = "vertices: "
        for k in self.vertices():
            res += str(k) + " "
            res += str(self.__coord_dict[k]) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res



