from ClusterGeneration.DistanceMatrix import generateDistanceMatrix
from Graphing.ConnectGraph import *
from Graphing.GeneratePOI import *
from Graphing.GraphConstructor import Graph


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


def constructGraph(nodeFile, edgeFile, directed=True):

    with open(nodeFile, "r") as n:
        vertices = n.readlines()

    with open(edgeFile, "r") as e:
        edges = e.readlines()


    g = dict()
    graph = Graph(g)

    """
    if directed:
        rg = dict()
        revGraph = Graph(rg)

        for v in vertices:
            [index, lon, lat] = v.split(" ")
            graph.add_vertex(index)
            revGraph.add_vertex(index)
            c = [float(lon), float(lat), 0]
            graph.add_coords(index, c)
            revGraph.add_coords(index, c)

        for e in edges:
            [index, outNode, inNode, length] = e.split(" ")
            graph.add_edge(outNode, [outNode, inNode, float(length)])
            revGraph.add_edge(inNode, [inNode, outNode, float(length)])

        return graph, revGraph
    """
    for v in vertices:
        [index, lon, lat] = v.split(" ")
        graph.add_vertex(index)
        c = [float(lon), float(lat), 0]
        graph.add_coords(index, c)

    for e in edges:
        [index, outNode, inNode, length] = e.split(" ")
        graph.add_edge(outNode, inNode, float(length))

    if not directed:
        for e in edges:
            [index, outNode, inNode, length] = e.split(" ")
            graph.add_edge(inNode, outNode, float(length))

    return graph


if __name__ == "__main__":
    file1 = "C:/Users/havar/Documents/MasterThesis/GraphData/la.cnode"
    file2 = "C:/Users/havar/Documents/MasterThesis/GraphData/la.cedge"
    directed = False
    Origgraph = constructGraph(file1, file2, directed)
    size = len(Origgraph.vertices())
    graphWithPOI = generatePOI(Origgraph, int(size/10), True)
    graphSplitNodes = duplicatePluralWeightedNodes(graphWithPOI)
    connectedGraph = connectGraph(graphSplitNodes, directed)

    distMatrix = generateDistanceMatrix(connectedGraph)
    for i in distMatrix.keys():
        print(i, end=': ')
        for j in distMatrix[i].keys():
                print(j, ": {0:.2f}".format(round(distMatrix[i][j], 3)), end = ', ')
        print()



