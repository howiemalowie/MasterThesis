# from GraphConstructor import Graph
import random
import numpy as np


def generatePOI(graph, amount, onSameNode=True):
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


"""
def removeEmptyNodes(graph, revGraph=None):
    if not revGraph is None:
        for v in graph.vertices():
            if graph.get_nodeweight(v) == 0:
                graph.remove_vertex(v, contract=True)
                revGraph.remove_vertex(v, contract=True)
    return graph, revGraph
"""
