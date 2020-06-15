import math
import random
import heapq as hq
import string

Inf = float("Inf")


def Dijkstra(G, s):
    b = G.get_base()
    vertices = G.vertices()
    visited = dict.fromkeys(vertices, False)
    dist = dict.fromkeys(vertices, Inf)
    sortedDist = dict()
    finalDist = dict.fromkeys([w for w in vertices if G.get_nodeweight(w) > 0 or w == b])
    Q = [(0.0, s)]

    while Q:
        (length, node) = hq.heappop(Q)
        visited[node] = True
        dist[node] = length

        if G.get_nodeweight(node) > 0 or node == b:
            finalDist[node] = dist[node]
            sortedDist[node] = dist[node]

        neighbors = G.get_neighbors(node)
        for n in neighbors:
            if not visited[n]:
                weight = G.get_edgeweight(node, n)
                if weight != -1:
                    if dist[n] > dist[node] + weight:
                        dist[n] = dist[node] + weight
                        hq.heappush(Q, (dist[n], n))

    return sortedDist, finalDist


def generateDistanceMatrix(graph):
    vertices = graph.vertices()
    b = graph.get_base()
    matrix = dict()
    sortedMatrix = dict()
    duped = dict()

    for v in vertices:
        dupes = graph.get_nodeweight(v)
        if dupes > 0 or v == b:
            sortedDist, finalDist = Dijkstra(graph, v)
            sortedMatrix[v] = sortedDist
            matrix[v] = finalDist
            order = 1
            duplicate_list = list()
            while order < dupes:
                new_ID = str(v) + get_name(order)
                sortedMatrix[new_ID] = sortedDist
                matrix[new_ID] = finalDist
                order += 1
                duplicate_list.append(new_ID)
            duped[v] = duplicate_list

    for v in duped.keys():
        for r in matrix.keys():
            add_to = dict.fromkeys(duped[v], matrix[r][v])
            matrix[r].update(add_to)

    return matrix, sortedMatrix


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
