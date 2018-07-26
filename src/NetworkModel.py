from numpy.core.multiarray import ndarray

import GlobalParameters as gp
import LinkService as linkService
from RadioModels import *
from collections import namedtuple
import numpy as np

# Initialize Global Parameters
gp.initializeGlobalParameters(MICA2)

def getFitnessForNetwork(nodeList):
    
    Fitness = namedtuple("Fitness", ["meanValidLinks"])
    
    linksForEachNode = linkService.getLinksForEachNode(nodeList)
    qualityLinksCounter = linkService.countLinksByQuality(linksForEachNode)
    meanQuality = linkService.getMeanQualityLinksForNetwork(qualityLinksCounter)
    
    qualityIndicators = Fitness(meanValidLinks=meanQuality)
    
    return qualityIndicators
    