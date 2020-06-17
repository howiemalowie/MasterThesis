from DistanceCalculation.DistanceMatrix import generateDistanceMatrix
from Graphing.ConnectGraph import *
from Graphing.GeneratePOI import *
from Graphing.GraphConstructor import Graph

import matplotlib.pyplot as plt


""" DEPRECATED FUNCTION"""
def duplicatePluralWeightedNodes(graph, revGraph=None):

    if revGraph is not None:

        for v in graph.vertices():
            w = graph.get_nodeweight(v)
            if w > 1:
                graph.duplicate_vertex(v, w)
                revGraph.duplicate_vertex(v, w)

        return graph, revGraph
    else:
        for v in graph.vertices():
            w = graph.get_nodeweight(v)
            if w > 1:
                graph.duplicate_vertex(v, w)

    return graph


""" 
Constructs a graph from input files of vertices and edges 
INPUT FORMAT VERTEX: "vertex_id, longitude, latitude, weight"
INPUT FORMAT EDGE: "edge_id, out_vertex, in_vertex, weight"
INPUT PARAMETER: State if graph is directed or not.
RETURN: graph if undirected + reverse graph if directed
"""
def constructGraph(nodeFile, edgeFile, directed=True):

    with open(nodeFile, "r") as n:
        vertices = n.readlines()

    with open(edgeFile, "r") as e:
        edges = e.readlines()

    graph = Graph()

    for v in vertices:
        [id, lon, lat] = v.split(" ")
        graph.add_vertex(id)
        c = [float(lon), float(lat), 0]
        graph.add_coords(id, c)

    for e in edges:
        [_, outNode, inNode, length] = e.split(" ")
        graph.add_edge(outNode, inNode, float(length))

    if not directed:
        for e in edges:
            [_, outNode, inNode, length] = e.split(" ")
            graph.add_edge(inNode, outNode, float(length))
        return graph

    else:
        revGraph = Graph()
        for v in vertices:
            [id, lon, lat] = v.split(" ")
            revGraph.add_vertex(id)
            c = [float(lon), float(lat), 0]
            revGraph.add_coords(id, c)

        for e in edges:
            [_, outNode, inNode, length] = e.split(" ")
            graph.add_edge(inNode, outNode, float(length))

        return graph, revGraph




def scatter_plot(graph, distMatrix):

    coords = graph.get_coord_dict()
    X = list()
    Y = list()

    for k in distMatrix.keys():
        [lon, lat, _] = coords[k]
        X.append(lon)
        Y.append(lat)

    Xmap = list()
    Ymap = list()
    for [lon, lat, _] in coords.values():
        Xmap.append(lon)
        Ymap.append(lat)

    plt.scatter(Xmap, Ymap, label="Road", color="green", marker=".", s=10)
    plt.scatter(X, Y, label="POI", color="red", marker="*", s=30)

    plt.xlabel('latitude')
    plt.ylabel('longitude')
    plt.title('Map of Greater Los Angeles')
    plt.legend()

    plt.show()


def main_test():
    file1 = "C:/Users/havar/Documents/MasterThesis/GraphData/la.cnode"
    file2 = "C:/Users/havar/Documents/MasterThesis/GraphData/la.cedge"
    tripLimit = 5
    directed = False
    graph = constructGraph(file1, file2, directed)
    size = len(graph.vertices())
    graph = connectGraph(graph)
    graph = generatePOI(graph, int(size/50), True)
    graph = duplicatePluralWeightedNodes(graph)
    distMatrix, sortedDistMatrix = generateDistanceMatrix(graph)
    #scatter_plot(graph, distMatrix)
    return sortedDistMatrix, tripLimit, graph.get_base()
    #Output formatting
    """
    print("Input:")
    print("maximum trip:", 8)
    
    for i in sortedDistMatrix.keys():
        print(i, end=': ')
        for j in sortedDistMatrix[i].keys():
                print(j, ": {0:.2f}".format(round(sortedDistMatrix[i][j], 3)), end = ', ')
        print()
    print()

    for i in distMatrix.keys():
        print(i, end=': ')
        for j in distMatrix[i].keys():
                print(j, ": {0:.2f}".format(round(distMatrix[i][j], 3)), end = ', ')
        print()
    print()
    print("Output:")
    lengths, trips = solveTrips(sortedDistMatrix, 8)
    print("total Distance:", round(sum(lengths), 3))
    for i, r in enumerate(trips):
        print("trip", i, "|", "length:", round(lengths[i], 3), r)
    """



