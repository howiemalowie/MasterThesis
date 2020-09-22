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
    D = 'D'
    visited = dict.fromkeys(dists, False)
    visited[D] = True
    n = len(dists)-1


    trips = list()
    triplengths = list()
    cnt = 0
    while cnt < n:
        currTrip = [D]
        length = 0
        tripCounter = 0
        currNode = D
        while tripCounter < tripLimit and cnt < n:
            nextNode = None
            for v in dists[currNode].keys():
                if not visited[v]:
                    nextNode = v
                    visited[v] = True
                    cnt += 1
                    break

            length += dists[currNode][nextNode]
            currTrip.append(nextNode)
            tripCounter += 1
            currNode = nextNode

        length += dists[currNode][D]
        currTrip.append(D)
        trips.append(currTrip)
        triplengths.append(length)

    return triplengths, trips
