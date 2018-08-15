from typing import List, Any, Callable
from src.model.NetNode import *
import numpy as np
import math
import src.model.GlobalParameters as gp
from collections import namedtuple

Bounds = namedtuple("Bounds",["upper","lower"])

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


def getLinksForEachNode(nodeList):
    """
    Get an array with link information for each node on the network.

    Each index in the array is a node. For it, each node has a list with all
    possible links. It's basically a list with a link with every other node on the
    network.

    In this list, is contained information about that link, such as the position
    of the receiver node, the link PRR and the link quality, based in the specified
    boundaries.

    CurrentNode: {
        links: [
            link1{
                NextNode,
                LinkQuality,
                LinkPRR,
                Link
            }
            link2...
        ]
    }

    :param nodeList: List of all nodes
    :return: array where each index is another array cont
    """

    if type(nodeList) is not np.ndarray:
        if type(nodeList) is list:
            nodeList = np.array(nodeList)
        else:
            raise TypeError("Argument object is not an array, and cannot be processed. Type: %s" %(type(nodeList)))

    LinkInfo = namedtuple("LinkInfo",["nextNode","linkQuality","linkPRR", "link"])
    NodeInfo = namedtuple("NodeInfo",["currentNode","links"])

    nodes = []

    for node in nodeList:
        nodeInfo = []
        links = getPossibleLinks(node, nodeList)
        for link in links:
            nextNode = link.nodeB
            linkPRR = calculateLinkPRR(link)
            quality = getLinkQuality(linkPRR, getPRRBounds())
            nodeInfo.append(LinkInfo(nextNode=nextNode, linkQuality=quality, linkPRR=linkPRR, link=link))
        nodes.append(NodeInfo(currentNode=node,links=nodeInfo))

    return nodes


def getLinkQuality(indicator, bounds):
    """
    Map an indicator value into a quality label based on the boundaries specified.

    :param indicator: The current quality indicator
    :param bounds: The quality boundaries.
    :return: "good", "medium" or "bad" based on the indicator value.
    """

    quality = ""
    if indicator >= bounds.upper:
        quality = "good"
    elif indicator <= bounds.lower:
        quality = "bad"
    else:
        quality = "medium"

    return quality


def getPossibleLinks(node: Node, nodeList):
    """
    Get a list with all possible links for a specified node.

    :param node: Current node to be evaluated.
    :param nodeList: List of all nodes within the network.
    :return: Numpy array with all links for the current node inside the network.
    """

    if type(nodeList) is not np.ndarray:
        if type(nodeList) is list:
            nodeList = np.array(nodeList)
        else:
            raise TypeError("Argument object is not an array, and cannot be processed")

    numberOfNodes = nodeList.size
    linkList = []

    for indexNode in range(0, numberOfNodes):
        if node is not nodeList[indexNode]:
            newLink = Link(node, nodeList[indexNode])
            linkList.append(newLink)

    linkList = np.array(linkList)
    return linkList


def countLinksByQuality(nodesInfo):
    """
    Method to count number of good, medium and bad links for each node. This will
    be useful to determine que quality of the network disposition, if we choose
    as a restriction a minimum number of good quality links for each node.

    :param nodesInfo: The array with the link information for each node. Can be
                        obtained through "getLinksForEachNode()" method.
    :return: An array whit each link quality counter for all nodes
    """

    QualityCounter = namedtuple("QualityCounter",["node", "good","medium","bad"])

    nodesQualityCounters = []

    for nodeInfo in nodesInfo:
        goodCounter = 0
        mediumCounter = 0
        badCounter = 0

        for linkInfo in nodeInfo.links:
            if linkInfo.linkQuality is "good":
                goodCounter += 1
            elif linkInfo.linkQuality is "medium":
                mediumCounter += 1
            elif linkInfo.linkQuality is "bad":
                badCounter += 1

        nodeQualityCounter = QualityCounter(node = nodeInfo.currentNode,
                                            good = goodCounter,
                                            medium = mediumCounter,
                                            bad = badCounter)
        nodesQualityCounters.append(nodeQualityCounter)

    return nodesQualityCounters


def getMeanQualityLinksForNetwork(nodesQualityCounters):
    
    meanValidLinks = lambda nodesQualityCounters: [(node.good + node.medium) for node in nodesQualityCounters]
    
    result = np.mean(meanValidLinks(nodesQualityCounters))
    
    return result
    
    
def calculateLinkPRR(link: Link):
    """
    This method calculates the Package Reception Ration for a specified link, according to the
    following formula:

                    1          SNR       B        8f
    PRR(d) = ( 1 - --- (exp(- ----- * ( --- ))) ) 
                    2           2        R
    
    :param:link: A default link object

    """

    SNR = getSNR(shadowing(link.distance))
    
    if SNR < 0:
        SNR = 0
        
    arg1 = np.float64(1.0 - 0.5 * (np.exp(-(SNR / 2.0) * (gp.Bn / gp.R))))
    arg2 = np.float64(8.0 * gp.arq)
    prr: np.float64 = np.power(arg1, arg2)

    return prr


def getSNR(Pr, PrInterf = 0):
    """
    Signal Noise Ratio basic calculation, defined as transmitted power divided
    by noise power (from other transmissions plus white noise power).

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
    pr = friss(gp.d0) * math.pow(10,getPahLoss(d)/10) #TODO: Terminar aqui

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

    SNRBounds = Bounds(upper=upperBound, lower=lowerBound)

    return SNRBounds


def getPRRBounds():
    prrBounds = Bounds(upper=0.9, lower=0.1)

    return prrBounds

# ============================| EXECUTION ROUTINE |=============================

if __name__ == '__main__':
    node1 = Node(0, 0)
    node2 = Node(0, 1)
    node3 = Node(1, 0)
    node4 = Node(1, 1)

    nodeList = np.array([node1, node2, node3, node4])
    l = getLinkList(nodeList)
