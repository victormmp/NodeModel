from src.NetNode import *
#from NetNode import *

import numpy as np
import math
from src.GlobalParameters import GlobalParameters as gp


def getLinkList(nodeList):
    """
    Generates a list with all possible links considering all nodes positions.

    :param nodeList: List of nodes. Contains all nodes positions on the
    distribuition.
    :return: Returns a list with all the possible links.
    """
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


def calculateLinkPRR(link):
    # TODO: Write consistent method

    SNR = getSNR()
    Arq = None
    prr = (1 - 0.5 * (math.exp(-(SNR / 2) * (1 / (gp.R / gp.Bn))))) ^ (8 * Arq)

    return prr


def getSNR():
    # TODO: Get consistent SNR function.

    pass


def friss(Pt, Gt, Gr, lamb, d, L):
    """
    Friss formula, used to determine the received power. Is defined as:

           Pt * Gt * Gr * lamb^2
    Pr = --------------------------
            (4 * pi * d)^2 * L

    :param Pt: Transmitted power
    :param Gt: Transmitter antenna gain
    :param Gr: Receiver antenna gain
    :param lamb: Transmitted signal wavelength
    :param d: Distance between receiver and transmitter
    :param L: System loss factor not related to propagation
    :return: Signal power at receiver
    """

    pr = (Pt * Gt * Gr * lamb) / ((4 * math.pi * d) ** 2 * L)

    return pr


def shadowing(Pt, lamb, d0, d, pathLossExp):
    pr = Pt * (lamb/4 * math.pi * d0)^2 * (d0 / d)^pathLossExp

    return pr


def getPahLoss():
    pass


################################################################################

if __name__ == '__main__':

    node1 = Node(0,0)
    node2 = Node(0,1)
    node3 = Node(1,0)
    node4 = Node(1,1)

    nodeList = np.array([node1,node2,node3,node4])
    l = getLinkList(nodeList)