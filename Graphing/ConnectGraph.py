""" AUTHOR: Haavard Notland"""

"""    
This class finds the strongly connected component of the depot vertex of the inputh graph
and removes all vertices not part of the obtained SCC from the input graph.
"""

""" 
Connects graph using two different methods: If input graph was directed, 
obtain the SCC of depot vertex using the reverse graph.
If undirected, remove all vertices not reached by depot using DFS.
"""


def connectGraph(graph, rev_graph=None):
    depot = graph.get_depot()
    visited = DFS(graph, depot)
    if rev_graph is not None:
        rev_visited = DFS(rev_graph, depot)
        for v in graph.vertices():
            if not visited[v] or not rev_visited[v]:
                graph.remove_vertex(v)

    else:
        for v in graph.vertices():
            if not visited[v]:
                graph.remove_vertex(v)


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
