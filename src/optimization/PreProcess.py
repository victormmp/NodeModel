

from src.model import LinkService as linkService, GlobalParameters as gp
from src.constants import *
from src.model.RadioModels import *
from src.model.NetNode import *
from collections import namedtuple
import numpy as np
import math
import matplotlib.pyplot as plt


def euclidian(vector1, vector2):
    assert len(vector1) == len(vector2)
    return math.sqrt(sum([(v1 - v2)**2 for v1, v2 in zip(vector1, vector2)]))

def direction(vector1, vector2):
    module = euclidian(vector1, vector2)
    return [(v2 - v1) / module for v1, v2 in zip(vector1, vector2)]

def next_point(point, direct, length):
    point = [coord + direct_coord * length for coord, direct_coord in zip(point, direct)]
    return point


def generateNodeListForInt(n: int, dim):
    """
    Get node list for a set of variables
    """
    N = []
    
    if n == 1:
        posX = (dim.end[0] - dim.start[0]) / 2.0
        posY = (dim.end[1] - dim.start[1]) / 2.0
        node = Node(posX, posY)
        N.append(node)
    elif n == 2:
        node1 = Node(xPos=dim.start[0], yPos=dim.start[1])
        node2 = Node(xPos=dim.end[0], yPos=dim.end[1])
        N.append(node1)
        N.append(node2)
    else:
        module =  euclidian(dim.start, dim.end)
        gap = module / (n-1)
        dirr = direction(dim.start, dim.end)

        node1 = Node(xPos=dim.start[0], yPos=dim.start[1])
        N.append(node1)

        for index in range(n-1):
            last = N[-1]
            nextCoord = next_point(last.getPoints(), dirr, gap)
            next = Node(nextCoord[0], nextCoord[1])
            N.append(next)
    
    return np.array(N)


if __name__ == '__main__':
    nodes = generateNodeListForInt(5, N2_DIM)
    x = [node.xPos for node in nodes]
    y = [node.yPos for node in nodes]
    plt.plot(x,y, 'o')
    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    plt.show()