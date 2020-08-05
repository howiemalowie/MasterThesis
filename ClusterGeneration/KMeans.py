import math
import heapq
import random
from ClusterGeneration.Cluster import Cluster
from ClusterGeneration.ClusterGroup import ClusterGroup


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
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def kmeans(graph, link_mat, k, lmt):
    coord_dict = graph.get_coord_dict()
    depot = graph.get_depot()
    clusters = dict()
    cluster_id = 0
    elementLookUp = dict.fromkeys(link_mat.keys(), None)

    # Randomly select k elements to be initial centroids
    lst = list(link_mat.keys())
    lst.remove(depot)
    random.shuffle(lst)
    for i in range(k):
        centroid = lst[i]
        clusters[str(cluster_id)] = Cluster(cluster_id, [depot, lst[i]], depot, centroid)
        cluster_id += 1

    done = False
    while not done:

        # Assign each point to cluster corresponding to the closest centroid that has not reached cluster size limit
        for key in link_mat.keys():
            if key == depot:
                continue

            distances = list()
            for c_ID in clusters.keys():
                centroid = clusters[c_ID].get_centroid()
                dist = link_mat[key][centroid] + link_mat[centroid][key] / 2
                heapq.heappush(distances, (dist, c_ID))

            while True:
                (_, closest_cluster_id) = heapq.heappop(distances)
                if clusters[closest_cluster_id].get_cluster_size() < lmt:
                    break

            remove_key = elementLookUp[key]
            if remove_key != closest_cluster_id and remove_key is not None:
                clusters[remove_key].remove_element(key)
                clusters[closest_cluster_id].add_element(key)
                elementLookUp[key] = closest_cluster_id

        # Update centroids. If no centroids change, end
        done = True
        for c in clusters.values():
            elements = c.get_elements()
            mean_lat = sum([coord_dict[p][0] for p in elements])/c.get_cluster_size()
            mean_lon = sum([coord_dict[p][1] for p in elements])/c.get_cluster_size()

            new_centroid = find_new_centroid(c, coord_dict, mean_lon, mean_lat)
            if new_centroid != c.get_centroid():
                done = False
                c.set_centroid(new_centroid)

    # Create clusterGroup once all clusters are finalized
    clusterGroup = ClusterGroup(link_mat, lmt, clusters)

    return clusterGroup
