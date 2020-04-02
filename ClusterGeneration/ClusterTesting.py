from Graphing.graphTesting import main_test
from ClusterGeneration.Clustering import Cluster

def buildClusters(matrix, clusterLimit):
    clusterList = []
    for k in matrix.keys():
        clusterList.append(Cluster(k))

    return clusterList

if __name__ == "__main__":
    matrix, clusterLimit = main_test()

    clusterList = buildClusters(matrix, clusterLimit)
