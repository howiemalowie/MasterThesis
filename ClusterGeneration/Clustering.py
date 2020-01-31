

def clusterBasedOnMatrix(sizeOfPlaneX, sizeOfPlaneY, coordinateList, matrix, clusterLimit):
    return divideCluster(coordinateList, clusterLimit, matrix)




# Recursive function that returns a list of clusters of size at most the clusterLimit
def divideCluster(cluster, clusterLimit, matrix):
    clusterList = list()
    cluster1 = list()
    cluster2 = list()
    # TODO: Divide cluster into two smaller clusters
    if(cluster1.length <= clusterLimit):
        clusterList.append(cluster1)
    else:
        clusterList.append(divideCluster(cluster1, clusterLimit, matrix))

    if (cluster2.length <= clusterLimit):
        clusterList.append(cluster2)
    else:
        clusterList.append(divideCluster(cluster2, clusterLimit, matrix))

    return clusterList



