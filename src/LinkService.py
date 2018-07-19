from NetNode import *
import numpy as np
import math
import logging
from GlobalParameters import GlobalParameters as gp

def getLinkList(nodeList):
    """
    Generates a list with all possible links considering all nodes positions.

    :param nodeList: List of nodes. Contains all nodes positions on the
    distribution.
    :return: Returns a list with all the possible links.
    """
    if type(nodeList) is not np.ndarray:
        if type(nodeList) is list:
            nodeList = np.array(nodeList)
        else:
            raise TypeError("Argument object is not an array, and cannot be processed")

    numberOfNodes = nodeList.size
    linkList = []

    for indexNodeA in range(0, numberOfNodes - 1):
        for indexNodeB in range(indexNodeA + 1, numberOfNodes):
            newLink = Link(nodeList[indexNodeA], nodeList[indexNodeB])
            linkList.append(newLink)

    linkList = np.array(linkList)

    print("Total number of links: ", linkList.size)
    return linkList


def getNetworkMeanPRR(linkList):
    """
    Get the mean PRR value for each link in the network.
    :param linkList: Lisk of all considered links.
    :return: Mean PRR value for the current network.
    """
    meanPRR = 0

    # Assert right object type

    if type(linkList) is not np.ndarray:
        if type(linkList) is list:
            linkList = np.array(linkList)
        else:
            raise TypeError("Argument object is not an array, and cannot be processed. Type: %s" %(type(linkList)))

    # Calculate mean PRR

    for index in range(0, linkList.size):
        meanPRR += calculateLinkPRR(linkList[index])
    meanPRR /= linkList.size

    return meanPRR


def calculateLinkPRR(link):
    #TODO: Verify error in this method and write docstring

    SNR = getSNR(shadowing(link.distance))
    prr = (1 - 0.5 * (math.exp(-(SNR / 2) * (1 / (gp.R / gp.Bn))))) ^ (8 * gp.arq)

    return prr


def getSNR(Pr, PrInterf = 0):
    """
    Signal Noise Ratio basic calculation, defined as transmitted power divided by noise power (from other transmissions
    plus white noise power).

                          Pr
    SNR (dB) = -------------------------
                (PrInterf + WhiteNoise)

    :param Pr: Transmitted power in Watts.
    :param PrInterf: Power from other transmissions interference. Typically zero.
    :return: Returns the white noise value in dB.
    """

    # snrPower = Pr/(PrInterf + gp.whiteNoiseVariance)
    snrPower = Pr - gp.whiteNoiseVariance
    snr = convertTodB(snrPower)

    return snr


def friss(d):
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

    pr = (gp.defaultPower * gp.Gt * gp.Gr * gp.lamb) / ((4 * math.pi * d) ** 2 * gp.L)

    return pr


def shadowing(d):
    #TODO: Get shadowing based on friss and PathLoss



    pr = gp.defaultPower - getPahLoss(d)
    # pr = friss(d) * math.pow(10,) #TODO: Terminar aqui

    # pr = gp.defaultPower * (gp.lamb / 4 * math.pi * gp.d0) ^ 2 * (gp.d0 / d) ^ gp.pathLossExp

    return pr


def getPahLoss(d):
    """
    Path loss attenuation in dB for a free space link. Can be calculated as:

                       Pr
    PL(dB) = - 10 log(----)
                       Pt
    or

                        Gt * Gr * lamb^2
    PL(dB) = -10 n log(------------------)
                         (4 * pi * d)^2

    :param Pt: Transmitter power
    :param Pr: Receiver power
    :return: Returns the path loss attenuation in dB
    """
    print(gp.whiteNoiseVariance)
    Xsig = np.random.normal(loc=0, scale=gp.whiteNoiseVariance)

    # pl = -10 * gp.pathLossExp * math.log10((gp.Gt * gp.Gr * gp.lamb^2)/((4 * math.pi * d)^2))
    pl = friss(d) + 10 * gp.pathLossExp * np.log10(d/gp.d0) + Xsig
    return pl


def convertTodB(value):
    """
    Returns the specified value in dB.
    :param value: The desired value to be converted
    :return: The value in dB
    """

    return 20 * math.log10(value)


# ============================| EXECUTION ROUTINE |=============================

if __name__ == '__main__':
    node1 = Node(0, 0)
    node2 = Node(0, 1)
    node3 = Node(1, 0)
    node4 = Node(1, 1)

    nodeList = np.array([node1, node2, node3, node4])
    l = getLinkList(nodeList)
