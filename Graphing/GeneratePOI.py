# from GraphConstructor import Graph
import geopy
import numpy as np
import geopy.distance
import random


def generateRandomPOI(graph, amount, onSameNode=True):
    vertices = graph.vertices()
    vertices.remove(graph.get_depot())
    sz = len(vertices)
    cnt = 0
    if onSameNode:

        distribution = np.random.dirichlet(np.ones(sz)) * amount

        for i, v in enumerate(vertices):
            weight = int(round(distribution[i]))
            cnt += weight
            graph.set_nodeweight(v, weight)

    else:

        distribution = np.ones(amount) + np.zeros(len(graph.vertices()) - amount)
        rand = random.shuffle(distribution)
        for i, v in enumerate(vertices):
            graph.set_nodeweight(rand[i])
            cnt += rand[i]
    return cnt


def generateClusteredPOI(graph, link_mat, amount, mean_lon, mean_lat, onSameNode=True):
    lst = list(link_mat.keys())
    coord_dict = graph.get_coord_dict()
    depot = graph.get_depot()
    lst.remove(depot)
    placed = dict()
    # First P.O.I. at the center of the graph
    min_dist = float("inf")
    first = ""
    for p in lst:
        lon = coord_dict[p][0]
        lat = coord_dict[p][1]
        dist = geo_dist(lon, lat, mean_lon, mean_lat)

        if dist < min_dist:
            first = p
            min_dist = dist

    S = list(range(1, 11))
    l = [0.2, 0.15, 0.2, 0.15, 0.1, 0.1, 0.025, 0.025, 0.025, 0.025]
    if onSameNode:
        cnt = np.random.choice(S, p=l)
        graph.set_nodeweight(first, cnt)
    else:
        cnt = 1
        graph.set_nodeweight(first, 1)
    placed[first] = True

    # Calculate probability
    D = [min(pow(link_mat[x][y], -1)*10 if link_mat[x][y] != 0.0 else 0.0 for y in placed.keys()) for x in lst]
    s = sum(D)
    P = [x / s for x in D]

    # Subsequent P.O.I.
    while cnt < amount:
        w = np.random.choice(lst, p=P)
        if onSameNode:
            POIS = np.random.choice(S, p=l)
            cnt += POIS
            graph.set_nodeweight(w, POIS)

        else:
            graph.set_nodeweight(w, 1)
            cnt += 1
        placed[w] = True

        # Update probabilities
        D = [min(pow(link_mat[x][y], -1)*1000 if link_mat[x][y] != 0.0 else 0.0 for y in placed.keys()) for x in lst]
        s = sum(D)
        if s == 0:
            break
        P = [x / s for x in D]
    return cnt


def geo_dist(x1, y1, x2, y2):
    return geopy.distance.distance((x1, y1), (x2, y2)).m

"""
def removeEmptyNodes(graph, revGraph=None):
    if not revGraph is None:
        for v in graph.vertices():
            if graph.get_nodeweight(v) == 0:
                graph.remove_vertex(v, contract=True)
                revGraph.remove_vertex(v, contract=True)
    return graph, revGraph
"""
