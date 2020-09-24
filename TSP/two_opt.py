
def swap(POI1, POI2, tour):
    reversed_part = tour[POI2:-len(tour) + POI1 - 1:-1]
    updated_tour = tour[:POI1] + reversed_part + tour[POI2+1:len(tour)]

    return updated_tour


def get_path_dist(tour, linkMat):
    dist = 0
    m = len(tour)-1
    for i in range(m):
        dist += linkMat[tour[i]][tour[i+1]]
    return dist


def two_opt(linkMat, init_tour, improve_threshold=0.000001):
    best_tour = init_tour
    best_dist = get_path_dist(best_tour, linkMat)
    num_POI = len(linkMat)
    improve_factor = 1

    while improve_factor > improve_threshold:
        prev_best = best_dist
        for i in range(1, num_POI-2):
            for j in range(i, num_POI-1):
                new_tour = swap(i, j, best_tour)
                new_dist = get_path_dist(new_tour, linkMat)
                if new_dist < best_dist:
                    best_tour = new_tour
                    best_dist = new_dist

        improve_factor = 1 - best_dist/prev_best

    return best_dist, best_tour
