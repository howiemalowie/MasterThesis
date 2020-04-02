"""
def solveTotalDist(dists, tripLimit):
    B = 'B'
    visited = dict.fromkeys(dists, False)
    visited[B] = True

    # Sort each row in matrix based on distance
    for d in dists.keys():
        dists[d] = {k: v for k, v in sorted(dists[d].items(), key=lambda item: item[1])}

    totalDist = 0
    while not all(visited[v] for v in visited):
        currTrip = 0
        currNode = B
        while currTrip < tripLimit and not all(visited[v] for v in visited):

            for v in dists[currNode].keys():
                if not visited[v]:
                    nextNode = v
                    visited[v] = True
                    break
            totalDist += dists[currNode][nextNode]
            currTrip += 1
            currNode = nextNode

        totalDist += dists[currNode][B]

    return totalDist
"""


def solveTrips(dists, tripLimit):
    B = 'B'
    visited = dict.fromkeys(dists, False)
    visited[B] = True

    # Sort each row in matrix based on distance (matrix already sorted)
    """
    for d in dists.keys():
        dists[d] = {k: v for k, v in sorted(dists[d].items(), key=lambda item: item[1])}
    """

    trips = list()
    triplengths = list()
    while not all(visited[v] for v in visited):
        currTrip = [B]
        length = 0
        tripCounter = 0
        currNode = B
        while tripCounter < tripLimit and not all(visited[v] for v in visited):
            nextNode = None
            for v in dists[currNode].keys():
                if not visited[v]:
                    nextNode = v
                    visited[v] = True
                    break

            length += dists[currNode][nextNode]
            currTrip.append(nextNode)
            tripCounter += 1
            currNode = nextNode

        length += dists[currNode][B]
        currTrip.append(B)
        trips.append(currTrip)
        triplengths.append(length)

    return triplengths, trips
