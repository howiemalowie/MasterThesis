import math
import random
import heapq as hq
import string

Inf = float("Inf")


def POI_Dijkstra(G, s):
    d = G.get_depot()
    vertices = G.vertices()
    visited = dict.fromkeys(vertices, False)
    dist = dict.fromkeys(vertices, Inf)
    sortedDist = dict()
    # finalDist = dict.fromkeys([w for w in vertices if G.get_nodeweight(w) > 0 or w == d])
    Q = [(0.0, s)]

    while Q:
        (length, node) = hq.heappop(Q)
        visited[node] = True
        dist[node] = length

        wght = G.get_nodeweight(node)
        if wght > 0 or node == d:
            # finalDist[node] = dist[node]
            sortedDist[node] = dist[node]
            for i in range(1, wght):
                new_ID = str(node) + get_name(i)
                sortedDist[new_ID] = dist[node]

        neighbors = G.get_neighbors(node)
        for n in neighbors:
            if not visited[n]:
                edge_weight = G.get_edgeweight(node, n)
                if edge_weight != -1:
                    if dist[n] > dist[node] + edge_weight:
                        dist[n] = dist[node] + edge_weight
                        hq.heappush(Q, (dist[n], n))

    return sortedDist


def Dijkstra(G, s):
    vertices = G.vertices()
    visited = dict.fromkeys(vertices, False)
    dist = dict.fromkeys(vertices, Inf)
    sortedDist = dict()
    # finalDist = dict.fromkeys([w for w in vertices if G.get_nodeweight(w) > 0 or w == d])
    Q = [(0.0, s)]

    while Q:
        (length, node) = hq.heappop(Q)
        visited[node] = True
        dist[node] = length
        # finalDist[node] = dist[node]
        sortedDist[node] = dist[node]

        neighbors = G.get_neighbors(node)
        for n in neighbors:
            if not visited[n]:
                edge_weight = G.get_edgeweight(node, n)
                if edge_weight != -1:
                    if dist[n] > dist[node] + edge_weight:
                        dist[n] = dist[node] + edge_weight
                        hq.heappush(Q, (dist[n], n))

    return sortedDist


def generateDistanceMatrix(graph):
    vertices = graph.vertices()
    d = graph.get_depot()
    sortedMatrix = dict()

    for v in vertices:
            wght = graph.get_nodeweight(v)
            if wght > 0 or v == d:
                sortedDist = POI_Dijkstra(graph, v)
                sortedMatrix[v] = sortedDist
                for i in range(1, wght):
                    new_ID = str(v) + get_name(i)
                    sortedMatrix[new_ID] = sortedDist

    return sortedMatrix


def generateFirstMatrix(graph):
    vertices = graph.vertices()
    sortedMatrix = dict()

    for v in vertices:
                sortedDist = Dijkstra(graph, v)
                sortedMatrix[v] = sortedDist

    return sortedMatrix


def get_name(num):

    num2alphadict = dict(zip(range(1, 27), string.ascii_lowercase))
    outval = ""
    numloops = (num-1) // 26

    if numloops > 0:
        outval = outval + get_name(numloops)

    remainder = num % 26
    if remainder > 0:
        outval = outval + num2alphadict[remainder]
    else:
        outval = outval + "z"
    return outval


# Generates a simple random distance matrix from input of dimensions of the plane and the number of elements
# Distance is calculated in a straight line and not from a graph
def generateRandomDistanceMatrix(sizeOfPlaneX, sizeOfPlaneY, nrOfElements):
    matrix = [[0 for x in range(nrOfElements)] for y in range(nrOfElements)]
    coordinateList = [[0 for x in range(3)] for y in range(nrOfElements)]

    # Assign random coordinates to elements
    for i in range(nrOfElements):
        coordinateList[i][0] = i
        coordinateList[i][1] = random.randint(0, sizeOfPlaneX)
        coordinateList[i][2] = random.randint(0, sizeOfPlaneY)

    # Calculate distance based on coordinates
    for i in range(nrOfElements):
        for j in range(nrOfElements):
            if i == j:
                matrix[i][j] = 0
            else:

                distance = math.sqrt(((coordinateList[i][1] - coordinateList[j][1]) ** 2) + (
                            (coordinateList[i][2] - coordinateList[j][2]) ** 2))
                matrix[i][j] = int(distance)

    return matrix, coordinateList
