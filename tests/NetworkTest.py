"""
Test file created to simulate operations with this network model
from a optimization algorithm.

Created by: Victor Magalhaes
"""
import sys

import click

import src.model.GlobalParameters as gp
import src.model.LinkService as linkService
import src.NetworkModel as NetworkModel
from src.model.GeoService import *
from src.model.RadioModels import *

sys.path.insert(0, r'../')



nodeArray: list = []

# ==============| TESTS |===============

def test1():
    """
    Test fitness calculation from a node list. The method being tested is supposed to be the
    main entry for the network model.
    """
    fitness = NetworkModel.getFitnessForNetwork(nodeArray)
    click.echo("Fitness: %s " % fitness.__str__())

    
def test2():
    """
    Test SRN for a random link of network list. The nodes are described as grid coordinates.
    """
    N = np.size(nodeArray)
    print(N)
    index = np.random.randint(0, N, size=2)
    print("index: ", index)
    nodeA = nodeArray[index[0]]
    nodeB = nodeArray[index[1]]
    snrTest = NetworkModel.getSNRForLink(nodeA, nodeB)
    
    print("For nodes: A(%s, %s)" %(nodeA.xPos, nodeA.yPos),
          " and B(%s, %s) " %(nodeB.xPos, nodeB.yPos), " - SNR: ", snrTest)
    

def test3():
    """
    Test if equality compare of two nodes are working correctly
    """
    
    print(nodeArray[1] is nodeArray[2])


def test4():
    """
    Test correct coordinate recovery from a geojson node distribution.
    """
    nodeList:list = getNodesFromGeoJSONFile('sample_geojson/sample_miranda_1.geojson')
    
    for item in nodeList:
        print (item.getCoordinates())


def test5():
    """
    Test SRN for a random link of network list. The nodes are 
    described as geographic coordinates.
    """
    N = np.size(nodeArray)
    print(N)
    index = np.random.randint(0, N, size=2)
    print("index: ", index)
    nodeA = nodeArray[index[0]]
    nodeB = nodeArray[index[1]]
    
    if nodeA is not nodeB:
        snrTest = NetworkModel.getSNRForLink(nodeA, nodeB)
        print("For nodes: A(%s, %s)" % (nodeA.latitude, nodeA.longitude),
              " and B(%s, %s) " % (nodeB.latitude, nodeB.longitude), " - SNR: ",
              snrTest)
    else:
        print("Same nodes: A(%s, %s)" % (nodeA.latitude, nodeA.longitude),
          " and B(%s, %s) " % (nodeB.latitude, nodeB.longitude))


def test6():
    """
    Test the number of links for each node groouped by quality.
    """

    # Initialize Global Parameters
    gp.initializeGlobalParameters(ZigBee)

    linkList = linkService.getLinkList(nodeArray)

    numberOfNodes = np.size(nodeArray)

    meanPRR = linkService.getNetworkMeanPRR(linkList)
    print("Number of nodes: ", numberOfNodes)
    print("Number of links: ", linkList.size)
    print("Mean PRR value: ", meanPRR)

    nodeLinks = linkService.getLinksForEachNode(nodeArray)

    nodesQuality = linkService.countLinksByQuality(nodeLinks)

    print("\n\n>> Quality links by node counter:\n")
    for node in nodesQuality:
        print("Node(%s, %s): Good: %s, Medium: %s, Bad: %s" %(node.node.xPos, node.node.yPos, node.good, node.medium, node.bad))


#==================================| COMMAND LINE ACCESS |===============================

@click.command('test-model')
@click.option('--test', '-t', type=click.STRING, required=True, multiple=False, help='Select the test you want to run.')
@click.pass_context
def init(context, test):

    global nodeArray
    click.clear()

    GEOJSON_FILE: str = './tests/sample_geojson/sample_miranda_2.geojson'
    # GEOJSON_FILE: str = None

    if GEOJSON_FILE is not None:
        nodeArray = getNodesFromGeoJSONFile(GEOJSON_FILE)
        click.secho('Using file: %s\n' % GEOJSON_FILE)
    else:
        N = 15
        for x in range(N):
            for y in range(N):
                nodeArray.append(Node(x,y))

    if test is None:
        click.secho('ERROR: no test informed.', fg='red', bold=True)

    click.secho('Selected Test: %s' %test, fg='green', bold=True)

    try:
        return {
            '1': test1,
            '2': test2,
            '3': test3,
            '4': test4,
            '5': test5,
            '6': test6
        }[test]()
    except KeyError:
        click.secho('ERROR: No test %s defined.' % test, fg='red', bold=True)

#==========| Test Selection |=========

if __name__=='__main__':
    init()
