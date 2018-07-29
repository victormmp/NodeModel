from model import LinkService as linkService, GlobalParameters as gp
from model.RadioModels import *
from model.NetNode import *
from collections import namedtuple
import numpy as np

# Initialize Global Parameters
gp.initializeGlobalParameters(ZigBee)

def getFitnessForNetwork(nodeList):
    
    Fitness = namedtuple("Fitness", ["meanValidLinks"])
    
    linksForEachNode = LinkService.getLinksForEachNode(nodeList)
    qualityLinksCounter = LinkService.countLinksByQuality(linksForEachNode)
    meanQuality = LinkService.getMeanQualityLinksForNetwork(qualityLinksCounter)
    
    qualityIndicators = Fitness(meanValidLinks=meanQuality)
    
    return qualityIndicators
    

def getSNRForLink(nodeA: Node, nodeB: Node):
    link: Link = Link(nodeA, nodeB)
    SNR = LinkService.getSNR(LinkService.shadowing(link.distance))
    
    return SNR