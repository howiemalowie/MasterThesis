import geopy.distance


if __name__ == "__main__" :
    node_file = "C:/Users/havar/Documents/MasterThesis/GraphData/mohlenpris.CNODE"
    edge_file = "C:/Users/havar/Documents/MasterThesis/GraphData/mohlenpris.CEDGE"

    with open(node_file, "r") as n:
        vertices = n.readlines()

    with open(edge_file, "r") as e:
        edges = e.readlines()

    with open("C:/Users/havar/Documents/MasterThesis/GraphData/weighted_mohlenpris.CEDGE", "w") as e2:
        for edge in edges:
            l = edge.split(" ")
            v1 = vertices[int(l[1])].split(" ")
            v2 = vertices[int(l[2])].split(" ")
            lat = float(v1[1])
            lng = float(v1[2])
            lat0 = float(v2[1])
            lng0 = float(v2[2])
            dist = round(geopy.distance.distance((lat, lng), (lat0, lng0)).m)
            e2.write(edge[:len(edge)-1] + " " + str(dist) + "\n")
