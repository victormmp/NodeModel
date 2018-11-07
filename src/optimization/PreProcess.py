

from src.model import LinkService as linkService, GlobalParameters as gp
from src.model.RadioModels import *
from src.model.NetNode import *
from settings import *
from collections import namedtuple
import numpy as np
import math
import matplotlib.pyplot as plt

dim = namedtuple("dim",["start", "end"])
area = namedtuple("area", ["top_left", "botom_right"])

# =====| Support methods|

def euclidian(vector1, vector2):
    assert len(vector1) == len(vector2)
    return math.sqrt(sum([(v1 - v2)**2 for v1, v2 in zip(vector1, vector2)]))

def direction(vector1, vector2):
    module = vincenty(vector1, vector2)*1000
    return [(v2 - v1) / module for v1, v2 in zip(vector1, vector2)]

def next_point(point, direct, length):
    point = [coord + direct_coord * length for coord, direct_coord in zip(point, direct)]
    return point

#=====

def generateNodeListForLine(n: int, dimension):
    """
    Get node list for a set of variables
    """
    N = []
    
    if n == 0:
        return np.array([])
    if n == 1:
        # posX = (dimension.end[0] - dimension.start[0]) / 2.0 + dimension.start[0]
        # posY = (dimension.end[1] - dimension.start[1]) / 2.0 + dimension.start[1]

        lon = (dimension.end[0] - dimension.start[0]) / 2.0 + dimension.start[0]
        lat = (dimension.end[1] - dimension.start[1]) / 2.0 + dimension.start[1]

        node = Node(latitude=lat, longitude=lon)
        N.append(node)
    elif n == 2:
        # node1 = Node(xPos=dimension.start[0], yPos=dimension.start[1])
        # node2 = Node(xPos=dimension.end[0], yPos=dimension.end[1])

        node1 = Node(latitude=dimension.start[0], longitude=dimension.start[1])
        node2 = Node(latitude=dimension.end[0], longitude=dimension.end[1])

        N.append(node1)
        N.append(node2)
    else:
        module =  vincenty(dimension.start, dimension.end)*1000
        gap = module / (n-1)
        dirr = direction(dimension.start, dimension.end)

        node1 = Node(latitude=dimension.start[0], longitude=dimension.start[1])
        N.append(node1)

        for _ in range(n-1):
            last = N[-1]
            nextCoord = next_point(last.getCoordinates(), dirr, gap)
            next = Node(latitude=nextCoord[0], longitude=nextCoord[1])
            N.append(next)
    
    return np.array(N)


def generateNodeListForArea(n: int, dimension):
    """
    Generate a grid of n x n nodes, within the specified grid area defined by dimension parameter.
    """

    if n == 1:
        dim_x = (dimension.top_left[0] + abs(dimension.top_left[0] - dimension.botom_right[0])) / 2
        area_dim = dim(start = (dim_x, dimension.top_left[1]),
                       end = (dim_x, dimension.botom_right[1]))
        return generateNodeListForLine(n, area_dim)

    
    up_dim = dim(start = (dimension.top_left), 
                    end = (dimension.botom_right[0],
                        dimension.top_left[1]))
    up_row = generateNodeListForLine(n, up_dim)

    low_dim = dim(start = (dimension.top_left[0], dimension.botom_right[1]), 
                    end = dimension.botom_right)
    low_row = generateNodeListForLine(n, low_dim)

    # dim_vector = [dim(start=lowNode.getPoints(), end=upNode.getPoints())
    #                     for lowNode, upNode in zip(low_row, up_row)]

    dim_vector = [dim(start=lowNode.getCoordinates(), end=upNode.getCoordinates())
                        for lowNode, upNode in zip(low_row, up_row)]
    
    columns = []

    for dim_item in dim_vector:
        column = generateNodeListForLine(n, dim_item)
        columns += column.tolist()

    return np.array(columns)


def ditributeNodesInArea(n: int, dimension):
    """
    Distribute n nodes inside all box area defined by the dimension parameter.
    The dimension must have the coordinates of the top-left and the botom-right vertices.

    This method return a numpy.ndarray object with all nodes.
    """

    if n <= 2:
        return generateNodeListForArea(n, dimension)
    
    


def generateNetworkForConstants(n1, n2, n3, n4):
    """
    Generate an identified set with each node distribution
    of the network.

    The input parameters are the number of nodes that compose each 
    distribution configuration.

    As an output, the method delivers the current network, splited in
    distribution areas in a dictionary object.
    """
    
    network = dict()
    network['SINK'] = gp.loadConstantsFromFile(CONSTANTS_FILE)
    network['N1'] = generateNodeListForLine(n1, gp.N1_DIM)
    network['N2'] = generateNodeListForLine(n2, gp.N2_DIM)
    network['N3'] = generateNodeListForLine(n3, gp.N3_DIM)
    network['N4'] = generateNodeListForArea(n4, gp.N4_DIM)

    return network