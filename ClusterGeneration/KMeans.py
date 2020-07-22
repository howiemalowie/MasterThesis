import random
import numpy as np
from ClusterGeneration.Cluster import Cluster


def kmeans(link_mat, k, lmt):

    clusters = dict()
    cluster_id = 0

    lst = link_mat.keys()
    lst.shuffle()
    for i in range(k):
        centroid = lst[i]
        clusters[str(cluster_id)] = Cluster(cluster_id, ['B', lst[i]], 'B', centroid)
        cluster_id += 1

    for key in link_mat.keys():
        distances = dict.fromkeys(link_mat, 0)
        for c in clusters.keys():
            centroid = clusters[c].get_centroid()
            distances[c] = ((link_mat[key][centroid] + link_mat[centroid][key]) / 2)

        closest_centroid_key = min(distances, key=distances.get)
        clusters[closest_centroid_key].add_element(key)

        #NEXT: update centroids

    return 0
