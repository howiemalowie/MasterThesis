import math
import xlsxwriter
from timeit import default_timer as timer

from ClusterGeneration.Agglomerate import buildClusters, agglomerate
from ClusterGeneration.GreedyClustering import greedy_clustering
from ClusterGeneration.GreedySolver import solveTrips
from ClusterGeneration.KMeans import kmeans
from Graphing.graphTesting import main_test
from TSP.TravelingSalesPerson import solve_all_clusters
from Experimentation.GoogleOR import OR



if __name__ == "__main__":
    workbook = xlsxwriter.Workbook('Mohlenpris.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', "Problem instance")
    worksheet.write('B1', "Size of input graph")
    worksheet.write('C1', "# of P.O.I.")
    worksheet.write('D1', "Tour limit")
    worksheet.write('E1', "Solving method")
    worksheet.write('F1', "Time to compute (milliseconds)")
    worksheet.write('G1', "Score (kilometers)")

    row = 1
    for prob_i in range(2):
        graph, matrix = main_test()
        d = graph.get_depot()
        graph_size = len(graph.vertices())
        n = len(matrix[d])
        tour_limit = [5, 10, 20]
        cost_func = ["CLINK", "K-SLINK", "K-CLINK"]
        inc_depot = [True, False]
        initiation = ["PLUSPLUS", "RANDOM"]
        coord_mat = graph.get_coord_dict()

        # OR
        for k in tour_limit:
            start = timer()
            res = OR(matrix, k, d)
            end = timer()

            worksheet.write(row, 0, prob_i+1)
            worksheet.write(row, 1, graph_size)
            worksheet.write(row, 2, n)
            worksheet.write(row, 3, k)
            worksheet.write(row, 4, "Google OR, local search w/ sim_annealing, 3 sec")
            worksheet.write(row, 5, (end - start)*1000 )
            worksheet.write(row, 6, round(res/1000, 3))
            row += 1

        print()

        # Naive solver
        for k in tour_limit:
            start = timer()
            lengths, trips = solveTrips(matrix, k)
            end = timer()
            print("NAIVE SOLVER result for k=", k)
            print(round(sum(lengths)/1000, 3), "km")
            #for i, r in enumerate(trips):
                #print("trip", i, "|", "length:", round(lengths[i], 3), r)
            worksheet.write(row, 0, prob_i + 1)
            worksheet.write(row, 1, graph_size)
            worksheet.write(row, 2, n)
            worksheet.write(row, 3, k)
            worksheet.write(row, 4, "Modified nearest neigbor")
            worksheet.write(row, 5, (end - start) * 1000)
            worksheet.write(row, 6, round(sum(lengths)/1000, 3))
            row += 1
        print()

        # NAIVE CLUSTERING
        for k in tour_limit:
            start = timer()
            greedyClusters = greedy_clustering(matrix, k, d)
            greedy_roots = greedyClusters.get_all_clusters().values()
            opt_cnt, hk_cnt = solve_all_clusters(greedyClusters, greedy_roots, d)
            end = timer()
            distance = 0

            if(opt_cnt == 0):
                solved = "Held-Karp"
            elif(hk_cnt == 0):
                solved = "2-opt"
            else:
                solved = "Mixed"

            for i, c in enumerate(greedy_roots):
                sol = c.get_solution()
                #print("trip", i, "|", "length:", round(sol[0], 3), sol[1])
                distance += sol[0]
            worksheet.write(row, 0, prob_i + 1)
            worksheet.write(row, 1, graph_size)
            worksheet.write(row, 2, n)
            worksheet.write(row, 3, k)
            worksheet.write(row, 4, solved + " Greedy clustering")
            worksheet.write(row, 5, (end - start) * 1000)
            worksheet.write(row, 6, round(distance/1000, 3))
            row += 1
            print("NAIVE CLUSTERING result for k=", k)
            print(round(distance/1000, 3), "km")


        print()

        # MAHC
        for k in tour_limit:
            best_distance = float("inf")
            for c in cost_func:
                for include in inc_depot:
                    start = timer()
                    MAH_Clusters = buildClusters(matrix, k, d, c, include)
                    agglomerate(MAH_Clusters, c, include)
                    roots = []
                    for clus in MAH_Clusters.get_all_clusters().values():
                        if clus.get_parent() is None:
                            roots.append(clus)

                    opt_cnt, hk_cnt = solve_all_clusters(MAH_Clusters, roots, d)
                    end = timer()
                    if (opt_cnt == 0):
                        solved = "Held-Karp"
                    elif (hk_cnt == 0):
                        solved = "2-opt"
                    else:
                        solved = "Mixed"

                    depot_inclusive = ""
                    if include:
                        depot_inclusive = "depot-inclusive-"
                    distance = 0
                    for i, clus in enumerate(roots):
                        sol = clus.get_solution()
                        distance += sol[0]
                        #print("trip", i, "|", "length:", round(sol[0], 3), sol[1])
                    print("MAHC result for k=", k, "cost-func=", c, "inc-depot=", include)
                    print(round(distance/1000, 3))
                    best_distance = min(distance, best_distance)
                    worksheet.write(row, 0, prob_i + 1)
                    worksheet.write(row, 1, graph_size)
                    worksheet.write(row, 2, n)
                    worksheet.write(row, 3, k)
                    worksheet.write(row, 4, solved + " Modified hierarchical clustering, cost function: " + depot_inclusive + c)
                    worksheet.write(row, 5, (end - start) * 1000)
                    worksheet.write(row, 6, round(distance / 1000, 3))
                    row += 1
            print("Best result from MAHC for k=", k)
            print(round(best_distance/1000, 3), "km")
        print()
    workbook.close()
    """
        #MKMC
        coord_dict = dict()
        for k in matrix.keys():
            if k == d:
                continue
            else:
                key = ''.join(ch for ch in k if ch.isdigit())
            coord_dict[k] = coord_mat[key]

        for k in tour_limit:
            best_distance = float("inf")
            start = math.ceil(n / k)
            stop = start + 4
            centroids = range(start, stop)
            for init in initiation:
                for K in centroids:
                    best_dist = float("inf")
                    best_time = 0
                    best_solved = ""
                    for i in range(3):
                        start = timer()
                        MKMC = kmeans(matrix, coord_dict, d, K, k, init)
                        MKMC_roots = MKMC.get_all_clusters().values()
                        opt_cnt, hk_cnt = solve_all_clusters(MKMC, MKMC_roots, d)
                        end = timer()
                        if (opt_cnt == 0):
                            solved = "Held-Karp"
                        elif (hk_cnt == 0):
                            solved = "2-opt"
                        else:
                            solved = "Mixed"
                        distance = 0
                        for i, clus in enumerate(MKMC_roots):
                            sol = clus.get_solution()
                            distance += sol[0]
                            #print("trip", i, "|", "length:", round(sol[0], 3), sol[1])
                        best_dist = min(distance, best_dist)
                        if distance < best_dist:
                            best_solved = solved
                            best_time = (end - start) * 1000
                        best_distance = min(best_dist, best_distance)
                    print("MKMC result for k=", k, "K=", K, "init=", init, "attempts=", 3)
                    print(round(best_dist / 1000, 3))
                    worksheet.write(row, 0, prob_i + 1)
                    worksheet.write(row, 1, graph_size)
                    worksheet.write(row, 2, n)
                    worksheet.write(row, 3, k)
                    worksheet.write(row, 4, best_solved + " Modified K-means clustering, initiation: " + init +
                                    ", centroids: " + str(K) + ", Cluster attempts: 3")
                    worksheet.write(row, 5, best_time)
                    worksheet.write(row, 6, round(best_dist / 1000, 3))
                    row += 1
            print("Best result from MKMC for k=", k)
            print(round(best_distance/1000, 3), "km")"""

