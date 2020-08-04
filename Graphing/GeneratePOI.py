# from GraphConstructor import Graph
import random
import numpy as np


def generatePOI(graph, amount, onSameNode=True):
    sz = len(graph.vertices())-1
    if onSameNode:

        distribution = np.random.dirichlet(np.ones(sz), size=amount)

        for v, i in enumerate(graph.vertices()):
            if v == graph.get_depot():
                i -= 1
            else:
                graph.set_nodeweight(round(distribution[i]))

    else:

        distribution = np.ones(amount) + np.zeros(len(graph.vertices()))
        rand = random.shuffle(distribution)
        for v, i in enumerate(graph.vertices()):
            if v == graph.get_depot():
                i -= 1
            else:
                graph.set_nodeweight(rand[i])

    return graph


"""
def removeEmptyNodes(graph, revGraph=None):
    if not revGraph is None:
        for v in graph.vertices():
            if graph.get_nodeweight(v) == 0:
                graph.remove_vertex(v, contract=True)
                revGraph.remove_vertex(v, contract=True)
    return graph, revGraph
"""
