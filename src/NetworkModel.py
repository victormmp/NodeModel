from model import LinkService as linkService, GlobalParameters as gp
from model.RadioModels import *
from model.NetNode import *
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
    print("Distance: ", link.distance)
    SNR = linkService.getSNR(linkService.shadowing(link.distance))
    
    return SNR