from src.NetNode import *
#from NetNode import *

import numpy as np


def getLinkList(nodeList):
    if type(nodeList) is not np.ndarray:
        nodeList = np.array(nodeList)

    numberOfNodes = nodeList.size
    linkList = []

    for indexNodeA in range(0, numberOfNodes-1):
        for indexNodeB in range(indexNodeA+1, numberOfNodes):
            newLink = Link(nodeList[indexNodeA], nodeList[indexNodeB])
            linkList.append(newLink)

    linkList = np.array(linkList)

    print("Total number of links: ", linkList.size)
    return linkList


if __name__ == '__main__':

    node1 = Node(0,0)
    node2 = Node(0,1)
    node3 = Node(1,0)
    node4 = Node(1,1)

    nodeList = np.array([node1,node2,node3,node4])
    l = getLinkList(nodeList)