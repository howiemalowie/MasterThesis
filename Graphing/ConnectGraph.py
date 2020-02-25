

def connectGraph(graph, revGraph=None):
    vertices = graph.vertices()
    # Find largest connected component
    largestComponent = 0
    largestStart = 0
    visited = dict()
    thisVisit = dict()
    for v in vertices:
        visited[v] = False
        thisVisit[v] = False

    if revGraph is None:
        for v in vertices:
            if not visited[v]:
                thisVisit = DFS(graph, v, visited, thisVisit)

                componentSize = 0
                for ele in vertices:
                    if thisVisit[ele]:
                        componentSize += 1

                if componentSize > largestComponent:
                    largestComponent = componentSize
                    largestStart = v

                thisVisit = dict.fromkeys(thisVisit, False)

        keepNodes = DFS(graph, largestStart, visited, thisVisit)
        removedNodes = 0
        for v in graph.vertices():
            # Remove vertex
            if not keepNodes[v]:
                graph.remove_vertex(v)
                removedNodes += 1
            # No need to update edges as any vertices
            # connected to this vertex is also removed
        return graph

    else:
        revThisVisit = thisVisit

        for v in vertices:
            if not visited[v]:
                thisVisit = dict.fromkeys(thisVisit, False)
                revThisVisit = dict.fromkeys(revThisVisit, False)
                thisVisit = DFS(graph, v, visited, thisVisit)
                revThisVisit = DFS(revGraph, v, visited, revThisVisit)

                componentSize = 0
                for ele in vertices:
                    if thisVisit[ele] and revThisVisit[ele]:
                        componentSize += 1

                if componentSize > largestComponent:
                    largestComponent = componentSize
                    largestStart = v

        thisVisit = dict.fromkeys(thisVisit, False)
        revThisVisit = dict.fromkeys(revThisVisit, False)

        keepNodes = DFS(graph, largestStart, visited, thisVisit)
        revKeepNodes = DFS(revGraph, largestStart, visited, revThisVisit)
        removedNodes = 0
        for v in graph.vertices():
            # Remove vertex
            if not keepNodes[v] or not revKeepNodes[v]:
                graph.remove_vertex(v)
                removedNodes += 1
            # No need to update edges as any vertices
            # connected to this vertex is also removed
        return graph


def DFS(graph, v, visited, currVisit):
    stack = list()
    visited[v] = True
    currVisit[v] = True
    stack.append(v)

    while stack:
        s = stack.pop()
        neighbors = graph.get_neighbors(s)
        for n in neighbors:
            if not currVisit[n]:
                stack.append(n)
                visited[n] = True
                currVisit[n] = True

    return currVisit
