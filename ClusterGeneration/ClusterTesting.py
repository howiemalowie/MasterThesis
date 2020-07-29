from ClusterGeneration.Agglomerate import buildClusters, agglomerate
from ClusterGeneration.GreedyClustering import greedy_clustering
from Graphing.graphTesting import main_test
from TSP.TravelingSalesPerson import solve_all_clusters

"""
def make_annotations(pos, text, M, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    labels = range(L)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations


def dendogram(Clusters):
    
    clusterList = Clusters.get_all_clusters()
    G = nx.Graph()
    G.add_nodes_from(clusterList.keys())
    G.add_node("root")
    roots = list()
    for k in clusterList.keys():
        children = clusterList[k].get_children()
        parent = clusterList[k].get_parent()
        if parent is not None:
            G.add_edge(parent, k)
        else:
            roots.append(k)

    for r in roots:
        G.add_edge("root", r)

    print("Nodes of graph: ")
    print(G.nodes())
    print("Edges of graph: ")
    print(G.edges())

    nx.draw(G)
    plt.show()
    
    clusterList = Clusters.get_all_clusters()
    nr_vertices = len(clusterList) + 1
    v_label = list(map(str, range(nr_vertices)))
    # Construct tree graph from clusterset
    G = Graph(directed=True)
    G.add_vertex()
    G.add_vertices(nr_vertices-1)

    idxof = dict()
    roots = list()

    for i, k in enumerate(clusterList.keys()):
        idxof[k] = i+1

    for i, k in enumerate(clusterList.keys()):
        parent = clusterList[k].get_parent()
        if parent is not None:
                idx = idxof[parent]
                G.add_edge(idx, i+1)
        else:
            roots.append(i+1)

    for r in roots:
        G.add_edge(0, r)

    lay = G.layout('rt')
    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G)
    E = [e.tuple for e in G.es]

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    labels = v_label

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title='Tree with Reingold-Tilford Layout',
                      annotations=make_annotations(position, v_label, M),
                      font_size=12,
                      showlegend=False,
                      xaxis=axis,
                      yaxis=axis,
                      margin=dict(l=40, r=40, b=85, t=100),
                      hovermode='closest',
                      plot_bgcolor='rgb(248,248,248)'
                      )
    fig.show()

    
    # Tree structure
    nodes = Clusters.get_all_clusters()
    leaves = set(n for n in nodes if n.get_children() is None)
    inner_nodes = set(n for n in nodes if n.get_children() is not None)

    # Compute size of each subtree
    subtree = dict((n, [n]) for n in leaves)
    for u in inner_nodes:
        children = set()
        while(len(nodes) > 0):
            v = nodes.pop()
            children.add(v)
            nodes += v.children()
        subtree[u] = sorted(children & leaves)

    # Order inner_nodes by subtree size, root is last
    inner_nodes.sort(key=lambda n: len(subtree[n]))

    leaves.sort()
    index = dict((tuple([n]), i) for i, n in enumerate(leaves))
    Z = []
    k = len(leaves)
    for i, n in enumerate(inner_nodes):
        children = n.get_children()
        x = children[0]
        for y in children[1:]:
            z = tuple(subtree[x] + subtree[y])
            i, j = index[tuple(subtree[x])], index[tuple(subtree[y])]
            Z.append([i, j, float(len(subtree[n])), len(z)])
            index[z] = k
            subtree[z] = list(z)
            x = z
            k += 1
    """


if __name__ == "__main__":
    graph, matrix, clusterLimit, b = main_test()

    Clusters = buildClusters(matrix, clusterLimit, b)
    coord_mat = graph.get_coord_dict()

    #print("merging clusters:")
    agglomerate(Clusters)

    greedyClusters = greedy_clustering(matrix, clusterLimit, b)
    print(greedyClusters)

    roots = []
    greedy_roots = greedyClusters.get_all_clusters().values()
    for c in Clusters.get_all_clusters().values():
        if c.get_parent() is None:
            roots.append(c)
            print(c)

    solve_all_clusters(Clusters, roots)
    sum = 0
    for c in roots:
        sol = c.get_solution()
        sum += sol[0]

    solve_all_clusters(greedyClusters, greedy_roots)
    greedy_sum = 0
    for c in greedy_roots:
        sol = c.get_solution()
        greedy_sum += sol[0]

    print("Cluster sum:", sum)
    print("Greedy sum:", greedy_sum)
