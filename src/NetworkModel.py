import GlobalParameters as gp
import LinkService as linkService
from RadioModels import *
from NetNode import *
from collections import namedtuple
import numpy as np

# Initialize Global Parameters
gp.initializeGlobalParameters(ZigBee)

def getFitnessForNetwork(nodeList):
    
    Fitness = namedtuple("Fitness", ["meanValidLinks"])
    
    linksForEachNode = linkService.getLinksForEachNode(nodeList)
    qualityLinksCounter = linkService.countLinksByQuality(linksForEachNode)
    meanQuality = linkService.getMeanQualityLinksForNetwork(qualityLinksCounter)
    
    qualityIndicators = Fitness(meanValidLinks=meanQuality)
    
    return qualityIndicators
    

def getSNRForLink(nodeA: Node, nodeB: Node):
    link: Link = Link(nodeA, nodeB)
    SNR = linkService.getSNR(linkService.shadowing(link.distance))
    
    return SNR