import itertools


def held_karp(M):
    lookup = list(M.keys())
    n = len(M)
    g = dict()

    for k in range(1, n):
        g[(1 << k, k)] = (M[lookup[0]][lookup[k]], 0)

    for S in range(2, n):
        for s in itertools.combinations(range(1, n), S):
            bits = 0
            for bit in s:
                bits |= 1 << bit
            for k in s:
                prev = bits & ~(1 << k)
                res = list()
                for m in s:
                    if m == 0 or m == k:
                        continue
                    res.append((g[(prev, m)][0] + M[lookup[m]][lookup[k]], m))
                g[(bits, k)] = min(res)

    bits = (2**n - 1) - 1
    res = list()

    for k in range(1, n):
        res.append((g[(bits, k)][0] + M[lookup[k]][lookup[0]], k))
    opt, parent = min(res)

    path = []
    for i in range(n - 1):
        path.append(lookup[parent])
        new_bits = bits & ~(1 << parent)
        _, parent = g[(bits, parent)]
        bits = new_bits

    path.append(lookup[0])
    return opt, list(reversed(path))

