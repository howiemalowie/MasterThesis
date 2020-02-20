from ClusterGeneration.DistanceMatrix import generateDistanceMatrix
from Graphing.ConnectGraph import connectGraph
from Graphing.GeneratePOI import generatePOI
from Graphing.GraphConstructor import Graph

def constructGraph(nodeFile, edgeFile, directed=True):

    with open(nodeFile, "r") as n:
        vertices = n.readlines()

    with open(edgeFile, "r") as e:
        edges = e.readlines()


    g = dict()
    graph = Graph(g)

    if directed:
        rg = dict()
        revGraph = Graph(rg)

        for v in vertices:
            [index, lon, lat] = list(map(float, v.split(" ")))
            graph.add_vertex(int(index))
            revGraph.add_vertex(int(index))
            c = [lon, lat, 0]
            graph.add_coords(int(index), c)
            revGraph.add_coords(int(index), c)

        for e in edges:
            [index, outNode, inNode, length] = list(map(float, e.split(" ")))
            graph.add_edge(int(outNode), [int(outNode), int(inNode), length])
            revGraph.add_edge(int(inNode), [int(inNode), int(outNode), length])

        graph = generatePOI(graph, int(len(graph.vertices()) / 2), False)
        graph = connectGraph(graph, revGraph)

        return graph

    else:
        for v in vertices:
            [index, lon, lat] = list(map(float, v.split(" ")))
            graph.add_vertex(int(index))
            c = [lon, lat, 0]
            graph.add_coords(int(index), c)

        for e in edges:
            [index, outNode, inNode, length] = list(map(float, e.split(" ")))
            graph.add_edge(int(outNode), [int(outNode), int(inNode), length])
            graph.add_edge(int(inNode), [int(inNode), int(outNode), length])

        graph = generatePOI(graph, int(len(graph.vertices()) / 2), False)
        graph = connectGraph(graph)

        return graph

if __name__ == "__main__":
    file1 = "C:/Users/havar/Documents/MasterThesis/cycle.cnode"
    file2 = "C:/Users/havar/Documents/MasterThesis/cycle.cedge"
    directed = True
    graph = constructGraph(file1, file2, directed)
    print(graph.__str__())
    distMatrix = generateDistanceMatrix(graph)
    for i in distMatrix.keys():
        print(distMatrix[i])




