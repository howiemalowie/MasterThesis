# from GraphConstructor import Graph
import random


def generatePOI(graph, amount, onSameNode=True):
    prob = amount / len(graph.vertices())
    done = False
    if onSameNode:
        while not done:
            rand = graph.vertices()
            random.shuffle(rand)
            for v in rand:
                if v != graph.get_depot():
                    if random.random() > prob:
                        w = graph.get_nodeweight(v) + 1
                        graph.set_nodeweight(v, w)
                        amount -= 1
                        if amount == 0:
                            done = True
                            break
                        prob = amount / len(graph.vertices())

    else:
        if prob > 1:
            for v in graph.vertices():
                if v != graph.get_depot():
                    graph.set_nodeweight(v, 1)
        else:
            while not done:
                rand = graph.vertices()
                random.shuffle(rand)
                for v in rand:
                    if graph.get_nodeweight(v) > 0:
                        continue
                    else:
                        if v != graph.get_depot():
                            if random.random() <= prob:
                                graph.set_nodeweight(v, 1)
                                amount -= 1
                                if amount == 0:
                                    done = True
                                    break
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
