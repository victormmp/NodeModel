""""
This module contains methods to be called by external processes, to access the network model
project. Through this, the optimization algorithm can access all network inner services.
"""


from src.model import LinkService as linkService, GlobalParameters as gp
from src.model.RadioModels import *
from src.model.NetNode import *
from src.optimization import PreProcess
from collections import namedtuple
from settings import *
import click

def getFitnessForNetwork(nodeList):
    """
    Calculate quality indicators for the current network. This can be used as a classification
    parameter, to compare with other networks.

    :param nodeList: The current network, described as a node arrange.
    :return: This method returns a namedtuple with all fitness indicators.
    """

    # Initialize Global Parameters
    gp.initializeGlobalParameters(ZigBee)
    
    Fitness = namedtuple("Fitness", ["meanValidLinks", "minValidLinks"])
    
    linksForEachNode = linkService.getLinksForEachNode(nodeList)
    qualityLinksCounter = linkService.countLinksByQuality(linksForEachNode)
    
    minPrr = linkService.getMinPRRForNetwork(linksForEachNode)
    meanQuality = linkService.getMeanQualityLinksForNetwork(qualityLinksCounter)
    minQuality = linkService.getMinQualityLinksForNetwork(qualityLinksCounter)
    
    qualityIndicators = Fitness(meanValidLinks=meanQuality, minValidLinks=minQuality, minPRR = minPrr)
    
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
    
    This method receives a set of parameters indicating the number of nodes at each
    possible diistribution previouly defined as alghorithm constants.

    The returned object is a fitness indicator.
    """

    # click.secho("\nGenerating fitness for variables", fg='yellow')
    # click.secho("For N1: %s nodes\nFor N2: %s nodes\nFor N3: %s nodes\nFor N4: %s x %s node grid\n" %(n1, n2, n3, n4, n4), fg='yellow')

    gp.loadConstantsFromFile(CONSTANTS_FILE)
    n1_nodes = PreProcess.generateNodeListForLine(n1, gp.N1_DIM)
    n2_nodes = PreProcess.generateNodeListForLine(n2, gp.N2_DIM)
    n3_nodes = PreProcess.generateNodeListForLine(n3, gp.N3_DIM)
    n4_nodes = PreProcess.generateNodeListForArea(n4, gp.N4_DIM)

    nodes = np.concatenate((n1_nodes, n2_nodes, n3_nodes, n4_nodes))

    fitness = getFitnessForNetwork(nodes)
    
    return fitness
