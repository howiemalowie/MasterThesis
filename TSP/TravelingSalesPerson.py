Inf = float("Inf")


def Exact_TSP(linkMat):
    n = len(linkMat)

    memo = {(tuple([k]), k): tuple([0, None]) for k in linkMat.keys()}
    queue = [(tuple([k]), k) for k in linkMat.keys()]

    while queue:
        prev_v, prev_lp = queue.pop(0)
        prev_d, _ = memo[(prev_v, prev_lp)]
        to_v = linkMat.keys().difference(set(prev_v))

        for new_lp in to_v:
            new_v = tuple(sorted(list(prev_v) + [new_lp]))
            new_d = prev_d + linkMat[prev_lp][new_lp]

            if (new_v, new_lp) not in memo:
                memo[(new_v, new_lp)] = (new_d, prev_lp)
                queue += [(new_v, new_lp)]
            elif new_d < memo[(new_v, new_lp)][0]:
                memo[new_v, new_lp] = (new_d, prev_lp)

    return retrace_optimal_path(memo, n)


def retrace_optimal_path(memo, n):
    ptr = tuple(range(n))
    fpm = dict((k, v) for k, v in memo.item()
               if k[0] == ptr)
    path_key = min(fpm.keys(), key=lambda x: fpm[x][0])

    lp = path_key[1]
    res, ntlp = memo[path_key]
    route = [lp]

    ptr = tuple(sorted(set(ptr).difference({lp})))
    while ntlp is not None:
        lp = ntlp
        path_key = (ptr, lp)
        _, ntlp = memo[path_key]

    route = [lp] + route
    return res, route


def extract_linkage_matrix(cluster, matrix):
    linkMat = dict()
    elements = cluster.get_elements()
    dummyStart = 's'
    dummyEnd = 'e'
    dummyBase = 'b2'
    for el in elements:
        row = dict()
        for ele in elements:
            row[ele] = matrix[el][ele]
        if el == cluster.get_base():
            row[dummyStart] = 0.0
            row[dummyEnd] = Inf
            linkMat[dummyBase] = row

        else:
            row[dummyStart] = Inf
            row[dummyEnd] = Inf
        linkMat[el] = row
    linkMat[dummyBase][dummyStart] = Inf
    linkMat[dummyBase][dummyEnd] = 0.0
    return linkMat


def find_optimal_clusters(queue):
    final_list = []
    while queue:
        cluster = queue.pop(0)
        children = cluster.get_children()

        if children is None:
            continue

        final_list.append(cluster)
        sum = 0
        for c in children:
            sum += c.get_solution[0]

        if sum < cluster.get_solution()[0]:
            p = cluster
            while p is not None:
                if sum < p.get_solution[0]:
                    final_list.remove(p)

                    newP = p.get_parent()
                    newC = newP.get_children()
                    newC.remove(p)
                    newC += p.get_children()

                    sum = 0
                    for c in newC:
                        sum += c.get_solution[0]

                    p = newP

                else:
                    break
        else:
            remove = True
            for c in children:
                if c.get_children() is not None:
                    remove = False
                    break
            if remove:
                for c in children:
                    final_list.remove(c)

    return final_list


def get_all_clusters_in_tree(clusters, curr):

    for c in curr.get_children():
        clusters += c

    for c in curr.get_children():
        get_all_clusters_in_tree(clusters, c)


def solve_all_clusters(clusterGroup, roots):
    matrix = clusterGroup.get_matrix()

    for c in clusterGroup.get_all_clusters().values():
        linkMat = extract_linkage_matrix(c, matrix)
        res, route = Exact_TSP(linkMat)
        c.set_solution([res, route])

    final_cluster_set = []
    for r in roots:
        clusters = [r]
        get_all_clusters_in_tree(clusters, r)

        final_cluster_set += find_optimal_clusters(clusters, r)







