"""
Test file created to simulate operations with this network model
from a optimization algorithm.

Created by: Victor Magalhaes
"""
import sys

sys.path.insert(0, r'../')

import src.NetworkModel as NetworkModel
from src.model.GeoService import *
import click

# ==========| Parameters |==========
#

nodeArray: list = []

GEOJSON_FILE: str = './tests/sample_geojson/sample_miranda_2.geojson'
# GEOJSON_FILE: str = None

if GEOJSON_FILE is not None:
    nodeArray = getNodesFromGeoJSONFile(GEOJSON_FILE)
else:
    N = 15
    for x in range(N):
        for y in range(N):
            nodeArray.append(Node(x,y))

# ==========| TEST 1 |==========
def test1():
    fitness = NetworkModel.getFitnessForNetwork(nodeArray)
    print("Fitness: ", fitness)

# ==========| TEST 2 |==========
def test2():
    N = np.size(nodeArray)
    print(N)
    index = np.random.randint(0, N, size=2)
    print("index: ", index)
    nodeA = nodeArray[index[0]]
    nodeB = nodeArray[index[1]]
    
    # nodeA = nodeArray[0]
    # nodeB = nodeArray[1]
    
    snrTest = NetworkModel.getSNRForLink(nodeA, nodeB)
    
    print("For nodes: A(%s, %s)" %(nodeA.xPos, nodeA.yPos),
          " and B(%s, %s) " %(nodeB.xPos, nodeB.yPos), " - SNR: ", snrTest)
    
# ==========| TEST 3 |==========
def test3():
    
    print(nodeArray[1] is nodeArray[2])

def test4():
    nodeList:list = getNodesFromGeoJSONFile('sample_geojson/sample_miranda_1.geojson')
    
    for item in nodeList:
        print (item.getCoordinates())

def test5():
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

@click.command('test')
@click.option('--test', '-t', type=click.STRING, required=True, multiple=False, help='Select the test you want to run.')
@click.pass_context
def init(context, test):

    if test is None:
        click.secho('ERROR: no test informed.', fg='red', bold=True)
        
    click.clear()
    click.secho('Selected Test: %s' %test, fg='green', bold=True)

    try:
        return {
            '1': test1,
            '2': test2,
            '3': test3,
            '4': test4,
            '5': test5
        }[test]()
    except KeyError:
        click.secho('ERROR: No test %s defined.' % test, fg='red', bold=True)

#==========| Test Selection |=========

if __name__=='__main__':
    init()