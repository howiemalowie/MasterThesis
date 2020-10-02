import math
import heapq
import sys

import geopy.distance
from numpy import random
from ClusterGeneration.Cluster import Cluster
from ClusterGeneration.ClusterGroup import ClusterGroup


def plusplus(link_mat, centroidLookUp, k, depot):
    lst = list(link_mat.keys())
    centroids = list()
    clusters = dict()
    lst.remove(depot)

    # First centroid
    idx = random.randint(0, len(lst)-1)
    clusters[str(0)] = Cluster(str(0), [depot, lst[idx]], depot, lst[idx])
    centroidLookUp[lst[idx]] = True
    centroids.append(lst[idx])

    # Calculate probability
    D = [min(link_mat[x][y] for y in centroids) for x in lst]
    s = sum(D)
    P = [x / s for x in D]
    whoops = False
    cont = 0
    # Subsequent centroids
    for i in range(1, k):
        x = list(range(len(P)))
        idx = random.choice(x, p=P)
        if centroidLookUp[lst[idx]]:
            print("double centroid")
        clusters[str(i)] = Cluster(str(i), [depot, lst[idx]], depot, lst[idx])
        centroidLookUp[lst[idx]] = True
        centroids.append(lst[idx])

        # Update probabilities
        D = [min(link_mat[x][y] for y in centroids) for x in lst]
        s = sum(D)
        if s == 0:
            whoops = True
            cont = i+1
            break
        P = [x / s for x in D]

    if whoops:
        for j in lst:
            if not centroidLookUp[j]:
                clusters[str(i)] = Cluster(str(cont), [depot, j], depot, j)
                centroidLookUp[j] = True
                cont = cont+1
            if cont >= k:
                break

    return clusters


def find_new_centroid(cluster, coord_dict, mean_lon, mean_lat):

    min_dist = float("inf")
    new_centroid = ""
    for p in cluster.get_elements():
        lon = coord_dict[p][0]
        lat = coord_dict[p][1]
        dist = euclid_dist(lon, lat, mean_lon, mean_lat)
        if dist < min_dist:
            new_centroid = p
            min_dist = dist

    return new_centroid


def euclid_dist(x1, y1, x2, y2):
    lat = x1 % 90
    lon = y1 % 90
    lat0 = x2 % 90
    lon0 = y2 % 90
    return geopy.distance.distance((lat, lon), (lat0, lon0)).m


def kmeans(link_mat, coord_dict, depot, K, lmt, init):

    centroidLookUp = dict.fromkeys(link_mat.keys(), False)
    if init == "RANDOM":
        clusters = dict()
        cluster_id = 0
        # Randomly select k elements to be initial centroids
        lst = list(link_mat.keys())
        lst.remove(depot)
        random.shuffle(lst)
        for i in range(K):
            clusters[str(cluster_id)] = Cluster(str(cluster_id), [depot, lst[i]], depot, lst[i])
            centroidLookUp[lst[i]] = True
            cluster_id += 1
    else:
        clusters = plusplus(link_mat, centroidLookUp, K, depot)

    done = False
    MAX_IT = 20
    cnt = 0
    while not done and cnt < MAX_IT:

        cnt += 1
        distances = list()
        # Assign each point to cluster corresponding to the closest centroid that has not reached cluster size limit
        for key in link_mat.keys():
            if key == depot or centroidLookUp[key]:
                continue

            for c_ID in clusters.keys():
                centroid = clusters[c_ID].get_centroid()
                dist = (link_mat[key][centroid] + link_mat[centroid][key]) / 2
                distances.append((dist, c_ID, key))
        heapq.heapify(distances)

        try:
            while distances:
                (_, closest_cluster_id, key) = heapq.heappop(distances)
                if clusters[closest_cluster_id].get_cluster_size() < lmt and not centroidLookUp[key]:
                    clusters[closest_cluster_id].add_element(key)
                    centroidLookUp[key] = True

        except IndexError:
            print("All P.O.I.", link_mat.keys())
            print("amount of P.O.I.", len(link_mat.keys())-1)
            #print("missing P.O.I.", key)
            print("K = ", K)
            print("k = ", lmt)
            for c in clusters.values():
                print(c)
                print(c.get_elements())
            sys.exit(1)

        # Update centroids. If no centroids change, end
        done = True
        centroidLookUp = dict.fromkeys(link_mat.keys(), False)
        for c in clusters.values():
            if c.get_cluster_size() == 0:
                continue
            elements = c.get_elements()
            mean_lat = 0
            mean_lon = 0
            for p in elements:
                if p == depot:
                    continue
                else:
                    coord_key = ''.join(ch for ch in p if ch.isdigit())
                mean_lat += coord_dict[coord_key][0]
                mean_lon += coord_dict[coord_key][1]

            mean_lat /= c.get_cluster_size()
            mean_lon /= c.get_cluster_size()

            new_centroid = find_new_centroid(c, coord_dict, mean_lon, mean_lat)
            old_centroid = c.get_centroid()
            if new_centroid != old_centroid:
                done = False
                c.set_centroid(new_centroid)
                centroidLookUp[new_centroid] = True
            else:
                centroidLookUp[old_centroid] = True

        if not done and cnt < MAX_IT:
            for c_key in clusters.keys():
                centroid = clusters[c_key].get_centroid()
                if centroid == depot:
                    clusters[c_key] = Cluster(c_key, [depot], depot, depot)
                else:
                    clusters[c_key] = Cluster(c_key, [depot, centroid], depot, centroid)

    # Create clusterGroup once all clusters are finalized
    clusterGroup = ClusterGroup(link_mat, lmt, clusters)

    return clusterGroup
