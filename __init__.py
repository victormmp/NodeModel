from model.LinkService import *
from model.NetNode import *
from model import GlobalParameters as gp, RadioModels
from model.GeoService import *

# Defining number of nodes as N^2
N = 9

# Initialize global Parameters
gp.initializeGlobalParameters(RadioModels.ZigBee)

nodeArray: list = []

GEOJSON_FILE: str = 'tests/sample_geojson/sample_miranda_2.geojson'
# GEOJSON_FILE = None

if GEOJSON_FILE is not None:
    nodeArray = getNodesFromGeoJSONFile(GEOJSON_FILE)
else:
    N = 11
    for x in range(N):
        for y in range(N):
            nodeArray.append(Node(x,y))
linkList = getLinkList(nodeArray)

numberOfNodes = np.size(nodeArray)

meanPRR = getNetworkMeanPRR(linkList)
print("Number of nodes: ", numberOfNodes)
print("Number of links: ", linkList.size)
print("Mean PRR value: ", meanPRR)

nodeLinks = getLinksForEachNode(nodeArray)

nodesQuality = countLinksByQuality(nodeLinks)

print("\n\n>> Quality links by node counter:\n")
for node in nodesQuality:
    print("Node(%s, %s): Good: %s, Medium: %s, Bad: %s" %(node.node.xPos, node.node.yPos, node.good, node.medium, node.bad))
