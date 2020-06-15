""" AUTHOR: Haavard Notland"""

"""    
This class finds the strongly connected component of the base vertex of the inputh graph
and removes all vertices not part of the obtained SCC from the input graph.
"""


def connectGraph(graph, rev_graph):
    base = graph.get_base()
    visited = DFS(graph, base)
    rev_visited = DFS(rev_graph, base)
    for v in graph.vertices():
        if not visited[v] or not rev_visited[v]:
            graph.remove_vertex(v)

    return graph


def DFS(graph, v):
    visited = dict.fromkeys(graph.vertices(), False)
    stack = [v]
    visited[v] = True

    while stack:
        s = stack.pop()
        neighbors = graph.get_neighbors(s)
        for n in neighbors:
            if not visited[n]:
                stack.append(n)
                visited[n] = True

    return visited
