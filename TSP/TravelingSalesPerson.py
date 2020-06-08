Inf = float("Inf")


def TSP(linkMat):
    n = len(linkMat)

    memo = {(tuple([k]), k): tuple([0, None]) for k in linkMat.keys()}
    queue = [(tuple([k]), k) for k in linkMat.keys()]

    while queue:
        prev_v, prev_lp = queue.pop(0)
        prev_d, _ =  memo[(prev_v, prev_lp)]
        to_v = linkMat.keys().difference(set(prev_v))

        for new_lp in to_v:
            new_v = tuple(sorted(list(prev_v) + [new_lp]))
            new_d = (prev_d + linkMat[prev_lp][new_lp])

            if (new_v, new_lp) not in memo:
                memo[(new_v, new_lp)] = (new_d, prev_lp)
                queue += [(new_v, new_lp)]
            elif new_d < memo[(new_v, new_lp)][0]:
                memo[new_v, new_lp] = (new_d, prev_lp)

    return retrace_optimal_path(memo, n)


def retrace_optimal_path(memo , n):
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



def solve_all_clusters(clusterGroup, roots):
    matrix = clusterGroup.get_matrix()
    for r in roots:
        dummyStart = 's'
        dummyEnd = 'e'
        dummyBase = 'b2'
        linkMat = dict()

        # Add dummy nodes before solving and extract local linkage matrix
        for e in r:
            row = dict()
            for el in r:
                row[el] = matrix[e][el]
            if e == r.get_base():
                row[dummyStart] = 0.0
                row[dummyEnd] = Inf
                linkMat[dummyBase] = row

            else:
                row[dummyStart] = Inf
                row[dummyEnd] = Inf
            linkMat[e] = row
        linkMat[dummyBase][dummyStart] = Inf
        linkMat[dummyBase][dummyEnd] = 0.0

        res, route = TSP(linkMat)
