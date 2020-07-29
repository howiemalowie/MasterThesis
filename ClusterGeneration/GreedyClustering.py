from ClusterGeneration.Cluster import Cluster
from ClusterGeneration.ClusterGroup import ClusterGroup


def greedy_clustering(link_mat, lmt, base):
    clusterList = dict()
    clusterID = 0
    clustered = dict.fromkeys(link_mat, False)
    clustered[base] = True
    for k in reversed(list(link_mat[base].keys())):
        if not clustered[k]:
            elem_list = [base, k]
            clustered[k] = True
            sz = 1
            for elm in link_mat[k].keys():
                if sz >= lmt:
                    break
                if not clustered[elm]:
                        elem_list.append(elm)
                        clustered[elm] = True
                        sz += 1

            clusterList[str(clusterID)] = Cluster(str(clusterID), elem_list, base)
            clusterID += 1
    clusterGroup = ClusterGroup(link_mat, lmt, clusterList)
    return clusterGroup

