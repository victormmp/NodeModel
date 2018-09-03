

from src.model import LinkService as linkService, GlobalParameters as gp
from src.constants import *
from src.model.RadioModels import *
from src.model.NetNode import *
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
    module = euclidian(vector1, vector2)
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
    
    if n == 1:
        posX = (dimension.end[0] - dimension.start[0]) / 2.0
        posY = (dimension.end[1] - dimension.start[1]) / 2.0
        node = Node(posX, posY)
        N.append(node)
    elif n == 2:
        node1 = Node(xPos=dimension.start[0], yPos=dimension.start[1])
        node2 = Node(xPos=dimension.end[0], yPos=dimension.end[1])
        N.append(node1)
        N.append(node2)
    else:
        module =  euclidian(dimension.start, dimension.end)
        gap = module / (n-1)
        dirr = direction(dimension.start, dimension.end)

        node1 = Node(xPos=dimension.start[0], yPos=dimension.start[1])
        N.append(node1)

        for _ in range(n-1):
            last = N[-1]
            nextCoord = next_point(last.getPoints(), dirr, gap)
            next = Node(nextCoord[0], nextCoord[1])
            N.append(next)
    
    return np.array(N)


def generateNodeListForArea(n: int, dimension):
    """
    Generate a grid of n x n nodes, within the specified grid area defined by dimension parameter.
    """
    
    up_dim = dim(start = (dimension.top_left), 
                    end = (dimension.botom_right[0],
                        dimension.top_left[1]))
    up_row = generateNodeListForLine(n, up_dim)

    low_dim = dim(start = (dimension.top_left[0], dimension.botom_right[1]), 
                    end = dimension.botom_right)
    low_row = generateNodeListForLine(n, low_dim)

    dim_vector = [dim(start=lowNode.getPoints(), end=upNode.getPoints())
                        for lowNode, upNode in zip(low_row, up_row)]
    
    columns = []

    for dim_item in dim_vector:
        column = generateNodeListForLine(n, dim_item)
        columns += column.tolist()

    return np.array(columns)
