def subGraphCoord(lonMax, lonMin, latMax, latMin, nodeFile, edgeFile):

    inBound = [False] * 21048
    with open(nodeFile, 'r') as r, open("la.cnode", 'w') as w:
        for line in r:
            pars = line
            [index, lon, lat] = list(map(float, pars.split(" ")))
            index = int(index)
            print(index, lon, lat)
            if lonMax >= lon >= lonMin and latMax >= lat >= latMin:
                w.write(line)
                inBound[index] = True

    with open(edgeFile, 'r') as r, open("la.cedge", 'w') as w:
        for line in r:
            pars = line
            [index, outNode, inNode, length] = list(map(float, pars.split(" ")))
            inNode = int(inNode)
            outNode = int(outNode)

            if inBound[inNode] and inBound[outNode]:
                w.write(line)



#TEST
lonMin = -118.641103
latMax = 34.334867
lonMax = -117.747091
latMin = 33.542474

nodeFile = "C:/Users/havar/Documents/MasterThesis/cal.cnode"
edgeFile = "C:/Users/havar/Documents/MasterThesis/cal.cedge"

subGraphCoord(lonMax, lonMin, latMax, latMin, nodeFile, edgeFile)