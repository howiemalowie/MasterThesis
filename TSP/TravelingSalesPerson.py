from TSP.DynProg import Exact_TSP
from TSP.two_opt import two_opt
from TSP.held_karp import held_karp


def extract_linkage_matrix(cluster, matrix):
    linkMat = dict()
    elements = cluster.get_elements()

    for el in elements:
        row = dict()
        for ele in elements:
            row[ele] = matrix[el][ele]
        linkMat[el] = row

    return linkMat


def nearest_neighbors(linkMat, d):
    init_tour = [d]
    visited = dict.fromkeys(linkMat, False)
    visited[d] = True
    curr = d
    while len(init_tour) < len(linkMat):
        for i in linkMat[curr].keys():
            if not visited[i]:
                init_tour.append(i)
                visited[i] = True
                curr = i
    init_tour.append(d)
    return init_tour


def solve_all_clusters(clusterGroup, roots, depot):
    matrix = clusterGroup.get_matrix()

    for r in roots:
        linkMat = extract_linkage_matrix(r, matrix)
        if len(linkMat) > 15:
            print("solving using 2-opt")
            init_tour = nearest_neighbors(linkMat, depot)
            res, tour = two_opt(linkMat, init_tour)
        else:
            print("solving using Held-Karp")
            res, tour = held_karp(linkMat)
        r.set_solution([res, tour])







