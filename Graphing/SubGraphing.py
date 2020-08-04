import random


def subGraphCoord(node_file, edge_file, random_bounds=False):

    if random_bounds:

        lon_min = random.uniform(-124.389343, -114.294258)
        lon_max = random.uniform(lon_min, -114.294258)
        lat_min = random.uniform(32.541302, 42.017231)
        lat_max = random.uniform(lat_min, 42.017231)

        write_node_file = "C:/Users/Havar/Documents/MasterThesis/GraphData/random.cnode"
        write_edge_file = "C:/Users/Havar/Documents/MasterThesis/GraphData/random.cedge"

    else:
        write_node_file = "C:/Users/Havar/Documents/MasterThesis/GraphData/la.cnode"
        write_edge_file = "C:/Users/Havar/Documents/MasterThesis/GraphData/la.cedge"

        lon_min = -118.641103
        lon_max = 34.334867
        lat_min = -117.747091
        lat_max = 33.542474
    success = False
    in_bound = [False] * 21048
    with open(node_file, 'r') as r, open(write_node_file, 'w') as w:
        for line in r:
            pars = line
            [index, lon, lat] = list(map(float, pars.split(" ")))
            index = int(index)
            if lon_max >= lon >= lon_min and lat_max >= lat >= lat_min:
                w.write(line)
                in_bound[index] = True
    if any(i for i in in_bound):
        success = True

    r.close()
    w.close()
    with open(edge_file, 'r') as r, open(write_edge_file, 'w') as w:
        for line in r:
            pars = line
            [index, outNode, inNode, length] = list(map(float, pars.split(" ")))
            inNode = int(inNode)
            outNode = int(outNode)

            if in_bound[inNode] and in_bound[outNode]:
                w.write(line)

    r.close()
    w.close()
    return success, write_node_file, write_edge_file
