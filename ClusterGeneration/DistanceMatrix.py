import math
import random


# Generates a simple random distance matrix from input of dimensions of the plane and the number of elements
# Distance is calculated in a straight line and not from a graph
def generateRandomDistanceMatrix(sizeOfPlaneX, sizeOfPlaneY, nrOfElements):
    matrix = [[0 for x in range(nrOfElements)] for y in range(nrOfElements)]
    coordinateList = [[0 for x in range(3)] for y in range(nrOfElements)]

    # Assign random coordinates to elements
    for i in range(nrOfElements):
        coordinateList[i][0] = i
        coordinateList[i][1] = random.randint(0, sizeOfPlaneX)
        coordinateList[i][2] = random.randint(0, sizeOfPlaneY)

    # Calculate distance based on coordinates
    for i in range(nrOfElements):
        for j in range(nrOfElements):
            if i == j:
                matrix[i][j] = 0
            else:

                distance = math.sqrt(((coordinateList[i][1] - coordinateList[j][1]) ** 2) + (
                            (coordinateList[i][2] - coordinateList[j][2]) ** 2))
                matrix[i][j] = int(distance)

    return matrix, coordinateList