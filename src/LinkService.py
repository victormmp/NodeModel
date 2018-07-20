from NetNode import *
import numpy as np
import math
import logging
import GlobalParameters as gp

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
    #TODO: Verify the equation. This power calculation results in a very large number

    SNR = getSNR(shadowing(link.distance))
    prr = np.power((1.0 - 0.5 * (np.exp(-(SNR / 2.0) * (gp.Bn / gp.R)))), (8.0 * gp.arq))

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

    snrPower = Pr/(PrInterf + gp.whiteNoiseVariance)
    # snrPower = Pr - gp.whiteNoiseVariance
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

    pr = (gp.defaultPower * gp.Gt * gp.Gr * np.power(gp.lamb, 2)) / (np.power((4 * math.pi * d) ,2) * gp.L)

    return pr


def shadowing(d):
    #TODO: Get shadowing based on friss and PathLoss

    pr0 = friss(d)

    # pr = convertTodBm(gp.defaultPower) - getPahLoss(d)
    pr = friss(d) * math.pow(10,getPahLoss(d)/10) #TODO: Terminar aqui

    # pr = gp.defaultPower * (gp.lamb / 4 * math.pi * gp.d0) ^ 2 * (gp.d0 / d) ^ gp.pathLossExp

    return pr


def getPahLoss(d):
    """
    Path loss attenuation in dB for a free space link. Can be calculated as:

                      Pr
    PL(d) = - 10 log(----)
                      Pt
    or

                       Gt * Gr * lamb^2
    PL(d) = -10 n log(------------------)
                        (4 * pi * d)^2
    or
                                     d
    PL(d) = PL(d0) + 10 * n * log10(----) + X_sigma
                                     d0

    :param Pt: Transmitter power
    :param Pr: Receiver power
    :return: Returns the path loss attenuation in dB
    """
    Xsig = np.random.normal(loc=0, scale=gp.std_db)

    pl = -10 * gp.pathLossExp * np.log10(d/gp.d0) + Xsig
    # pl = -10 * gp.pathLossExp * np.log10((gp.Gt * gp.Gr * np.power(gp.lamb,2))/np.power((4 * math.pi * d),2))
    # pl = friss(d) + 10 * gp.pathLossExp * np.log10(d/gp.d0) + Xsig
    return pl


def convertTodB(value):
    """
    Returns the specified value in dB.
    :param value: The desired value to be converted
    :return: The value in dB
    """

    return 20.0 * np.log10(value)


def convertTodBm(value):

    dBm = 20 * np.log10(value/1e3)

    return dBm

def getSNRBounds():
    upperBound = 10 * np.log10(-1.28 * np.log(1 - np.power(0.9, (1 / (8 * gp.arq)))))
    lowerBound = 10 * np.log10(-1.28 * np.log(1 - np.power(0.1, (1 / (8 * gp.arq)))))

    pass #TODO: Make a return as an object like bound.upper


# ============================| EXECUTION ROUTINE |=============================

if __name__ == '__main__':
    node1 = Node(0, 0)
    node2 = Node(0, 1)
    node3 = Node(1, 0)
    node4 = Node(1, 1)

    nodeList = np.array([node1, node2, node3, node4])
    l = getLinkList(nodeList)
