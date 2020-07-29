import math
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

    return math.sqrt(pow(x1 - x2) + pow(y1 - y2))


def kmeans(link_mat, coord_dict, k, lmt):

    clusters = dict()
    cluster_id = 0
    elementLookUp = dict.fromkeys(link_mat.keys(), "0")

    # Randomly select k elements to be initial centroids
    lst = link_mat.keys()
    lst.shuffle()
    for i in range(k):
        centroid = lst[i]
        clusters[str(cluster_id)] = Cluster(cluster_id, ['B', lst[i]], 'B', centroid)
        cluster_id += 1

    done = False
    while not done:

        # Assign each point to cluster corresponding to the closest centroid
        for key in link_mat.keys():
            if key == 'B':
                continue

            distances = dict.fromkeys(clusters.keys(), float("inf"))
            for c in clusters.keys():
                centroid = clusters[c].get_centroid()
                distances[c] = ((link_mat[key][centroid] + link_mat[centroid][key]) / 2)

            closest_centroid = min(distances, key=distances.get)
            clusters[elementLookUp[key]].remove_element(key)
            clusters[closest_centroid].add_element(key)
            elementLookUp[key] = closest_centroid

        # Update centroids. If no centroids change, end
        done = True
        for c in clusters.values():
            mean_lat = sum([coord_dict[p][0] for p in c.get_elements()])/c.get_cluster_size()
            mean_lon = sum([coord_dict[p][1] for p in c.get_elements()])/c.get_cluster_size()

            new_centroid = find_new_centroid(c, coord_dict, mean_lon, mean_lat)
            if new_centroid != c.get_centroid():
                done = False
                c.set_centroid(new_centroid)

    # Create clusterGroup once all clusters are finalized
    clusterGroup = ClusterGroup(link_mat, lmt, clusters)

    return clusterGroup
