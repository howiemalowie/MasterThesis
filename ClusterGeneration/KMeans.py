import math
import heapq
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
    # Subsequent centroids
    for i in range(1, k):
        x = list(range(len(P)))
        [idx] = random.choice(x, 1, P)
        clusters[str(i)] = Cluster(str(i), [depot, lst[idx]], depot, lst[idx])
        centroidLookUp[lst[idx]] = True
        centroids.append(lst[idx])

        # Update probabilities
        D = [min(link_mat[x][y] for y in centroids) for x in lst]
        s = sum(D)
        P = [x / s for x in D]

    return clusters


def find_new_centroid(cluster, coord_dict, mean_lon, mean_lat):

    min_dist = float("inf")
    new_centroid = ""
    for p in cluster.get_elements():
        if p == cluster.get_depot():
            continue
        else:
            coord_key = ''.join(ch for ch in p if ch.isdigit())

        lon = coord_dict[coord_key][0]
        lat = coord_dict[coord_key][1]
        dist = euclid_dist(lon, lat, mean_lon, mean_lat)
        if dist < min_dist:
            new_centroid = p
            min_dist = dist

    return new_centroid


def euclid_dist(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


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
    while not done:

        # Assign each point to cluster corresponding to the closest centroid that has not reached cluster size limit
        for key in link_mat.keys():
            if key == depot or centroidLookUp[key]:
                continue

            distances = list()
            for c_ID in clusters.keys():
                centroid = clusters[c_ID].get_centroid()
                dist = link_mat[key][centroid] + link_mat[centroid][key] / 2
                heapq.heappush(distances, (dist, c_ID))
                distances.append((dist, c_ID))
            heapq.heapify(distances)

            while True:
                (_, closest_cluster_id) = heapq.heappop(distances)
                if clusters[closest_cluster_id].get_cluster_size() < lmt:
                    clusters[closest_cluster_id].add_element(key)
                    break

        # Update centroids. If no centroids change, end
        done = True
        for c in clusters.values():
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
                centroidLookUp[old_centroid] = False
                centroidLookUp[new_centroid] = True

        if not done:
            for c_key in clusters.keys():
                centroid = clusters[c_key].get_centroid()
                if centroid == depot:
                    clusters[c_key] = Cluster(c_key, [depot], depot, depot)
                else:
                    clusters[c_key] = Cluster(c_key, [depot, centroid], depot, centroid)

    # Create clusterGroup once all clusters are finalized
    clusterGroup = ClusterGroup(link_mat, lmt, clusters)

    return clusterGroup
