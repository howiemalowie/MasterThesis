

def connectGraph(graph, directed=False):
    # Removes vertices not strongly connected to base
    base = graph.get_base()
    visited = DFS(graph, base)
    removeGraph = dict.fromkeys(graph.vertices(), False)
    for v in visited:
        if visited[v]:
            if directed:
                thisVisit = DFS(graph, v)
                if not thisVisit[base]:
                    removeGraph[v] = True
        else:
            removeGraph[v] = True

    for r in removeGraph:
        if removeGraph[r]:
            graph.remove_vertex(r)

        """
        for v in vertices:
            if not visited[v]:
                thisVisit = dict.fromkeys(thisVisit, False)
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
        """

        """        
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
        """

    return graph


def DFS(graph, v):
    visited = dict.fromkeys(graph.vertices(), False)
    stack = list()
    stack.append(v)
    visited[v] = True

    while stack:
        s = stack.pop()
        neighbors = graph.get_neighbors(s)
        for n in neighbors:
            if not visited[n]:
                stack.append(n)
                visited[n] = True

    return visited
