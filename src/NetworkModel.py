""""
This module contains methods to be called by external processes, to access the network model
project. Through this, the optimization algorithm can access all network inner services.
"""


from src.model import LinkService as linkService, GlobalParameters as gp
from src.constants import *
from src.model.RadioModels import *
from src.model.NetNode import *
from src.optimization import PreProcess
from collections import namedtuple

def getFitnessForNetwork(nodeList):
    """
    Calculate quality indicators for the current network. This can be used as a classification
    parameter, to compare with other networks.

    :param nodeList: The current network, described as a node arrange.
    :return: This method returns a namedtuple with all fitness indicators.
    """

    # Initialize Global Parameters
    gp.initializeGlobalParameters(ZigBee)
    
    Fitness = namedtuple("Fitness", ["meanValidLinks"])
    
    linksForEachNode = linkService.getLinksForEachNode(nodeList)
    qualityLinksCounter = linkService.countLinksByQuality(linksForEachNode)
    meanQuality = linkService.getMeanQualityLinksForNetwork(qualityLinksCounter)
    
    qualityIndicators = Fitness(meanValidLinks=meanQuality)
    
    return qualityIndicators
    

def getSNRForLink(nodeA: Node, nodeB: Node):
    """
    This method returns the calculated SNR for two nodes. 
    """

    # Initialize Global Parameters
    gp.initializeGlobalParameters(ZigBee)

    link: Link = Link(nodeA, nodeB)
    print("Distance: ", link.distance)
    SNR = linkService.getSNR(linkService.shadowing(link.distance))
    
    return SNR

def getFitnessForVariables(n1: int, n2: int, n3: int, n4: int):
    """
    Get fitness for a set of variables.
    """

    n1_nodes = PreProcess.generateNodeListForLine(n1, N1_DIM)
    n2_nodes = PreProcess.generateNodeListForLine(n2, N2_DIM)
    n3_nodes = PreProcess.generateNodeListForLine(n3, N3_DIM)
    n4_nodes = PreProcess.generateNodeListForArea(n4, N4_DIM)

    nodes = np.concatenate((n1_nodes, n2_nodes, n3_nodes, n4_nodes))

    getFitnessForNetwork(nodes)
    

