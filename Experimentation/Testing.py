import math

from ClusterGeneration.Agglomerate import buildClusters, agglomerate
from ClusterGeneration.GreedyClustering import greedy_clustering
from ClusterGeneration.GreedySolver import solveTrips
from ClusterGeneration.KMeans import kmeans
from Graphing.graphTesting import main_test
from TSP.TravelingSalesPerson import solve_all_clusters



if __name__ == "__main__":
    graph, matrix = main_test()
    d = graph.get_depot()
    n = len(matrix(d))
    tour_limit = [7, 17, 27]
    cost_func = ["CLINK", "K-SLINK", "K-CLINK"]
    inc_depot = [True, False]
    initiation = ["RANDOM", "PLUSPLUS"]
    coord_mat = graph.get_coord_dict()


    # Naive solver
    for k in tour_limit:
        lengths, trips = solveTrips(matrix, k)
        print("NAIVE SOLVER result for k=", k)
        print(round(sum(lengths), 3))

    # NAIVE CLUSTERING
    for k in tour_limit:
        greedyClusters = greedy_clustering(matrix, k, d)
        greedy_roots = greedyClusters.get_all_clusters().values()
        solve_all_clusters(greedyClusters, greedy_roots)
        distance = 0
        for c in greedy_roots:
            sol = c.get_solution()
            distance += sol[0]
            print("NAIVE CLUSTERING result for k=", k)
            print(round(distance, 3))

    # MAHC
    for k in tour_limit:
        for c in cost_func:
            for include in inc_depot:

                MAH_Clusters = buildClusters(matrix, k, d)
                agglomerate(MAH_Clusters, c, include)
                roots = []
                for clus in MAH_Clusters.get_all_clusters().values():
                    if clus.get_parent() is None:
                        roots.append(clus)

                solve_all_clusters(MAH_Clusters, roots)
                distance = 0
                for clus in roots:
                    sol = clus.get_solution()
                    distance += sol[0]
                print("MAHC result for k=", k, "cost-func=", c, "inc-depot=", include)
                print(round(distance, 3))

    #MKMC
    for k in tour_limit:
        start = math.ceil(n / k)
        stop = start + 5
        centroids = range(math.ceil(n/k), stop)
        for init in initiation:
            for K in centroids:
                best_dist = float("inf")
                for i in range(3):
                    MKMC = kmeans(matrix, coord_mat, d, K, k, init)
                    MKMC_roots = MKMC.get_all_clusters().values()
                    solve_all_clusters(MKMC, MKMC_roots)
                    distance = 0
                    for clus in MKMC_roots:
                        sol = clus.get_solution()
                        distance += sol[0]
                    best_dist = min(distance, best_dist)
                print("MAHC result for k=", k, "K=", K, "init=", init, "attempts=", 3)
                print(round(best_dist, 3))
