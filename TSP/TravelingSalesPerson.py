from TSP.DynProg import Exact_TSP
from TSP.two_opt import two_opt


def extract_linkage_matrix(cluster, matrix):
    linkMat = dict()
    elements = cluster.get_elements()

    for el in elements:
        row = dict()
        for ele in elements:
            row[ele] = matrix[el][ele]
        linkMat[el] = row

    return linkMat


def nearest_neighbors(linkMat):
    init_tour = ['D']
    visited = dict.fromkeys(linkMat, False)
    visited['D'] = True
    curr = 'D'
    while len(init_tour) < len(linkMat):
        for i in linkMat[curr].keys():
            if not visited[i]:
                init_tour.append(i)
                visited[i] = True
                curr = i
    init_tour.append('D')
    return init_tour


def solve_all_clusters(clusterGroup, roots):
    matrix = clusterGroup.get_matrix()

    for r in roots:
        linkMat = extract_linkage_matrix(r, matrix)
        init_tour = nearest_neighbors(linkMat)
        res, tour = two_opt(linkMat, init_tour)
        r.set_solution([res, tour])







