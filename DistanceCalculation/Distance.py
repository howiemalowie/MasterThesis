

def complete_linkage_clustering(cluster1, cluster2, matrix, inc_depot=False):
    elems1 = cluster1.get_elements()
    elems2 = cluster2.get_elements()
    max_dist = 0
    for e1 in elems1:
        if e1 == cluster1.get_depot() and not inc_depot:
            continue
        for e2 in elems2:
            if e2 == cluster2.get_depot() and not inc_depot:
                continue
            new_dist = (matrix[e1][e2] + matrix[e2][e1]) / 2
            max_dist = max(max_dist, new_dist)
    return max_dist


def K_single_linkage_clustering(cluster1, cluster2, matrix, k, inc_depot=False):
    elems1 = cluster1.get_elements()
    elems2 = cluster2.get_elements()
    dists = list()
    for e1 in elems1:
        if e1 == cluster1.get_depot() and not inc_depot:
            continue
        for e2 in elems2:
            if e1 == cluster1.get_depot() and e2 == cluster2.get_depot():
                continue
            dists.append((matrix[e1][e2] + matrix[e2][e1]) / 2)
    dists.sort()
    return sum(dists[:k])/k


def K_complete_linkage_clustering(cluster1, cluster2, matrix, k, inc_depot=False):
    elems1 = cluster1.get_elements()
    elems2 = cluster2.get_elements()
    dists = list()
    for e1 in elems1:
        if e1 == cluster1.get_depot() and not inc_depot:
            continue
        for e2 in elems2:
            if e1 == cluster1.get_depot() and e2 == cluster2.get_depot():
                continue
            dists.append((matrix[e1][e2] + matrix[e2][e1]) / 2)
    dists.sort(reverse=True)
    return sum(dists[:k]) / k
