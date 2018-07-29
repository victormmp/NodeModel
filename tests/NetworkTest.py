"""
Test file created to simulate operations with this network model
from a optimization algorithm.

Created by: Victor Magalhaes
"""

import NetworkModel
from model.NetNode import *
import numpy as np

# ==========| Parameters |==========
#
N = 9

nodeArray = []

for x in range(N):
    for y in range(N):
        nodeArray.append(Node(x,y))
        
TEST_1 = 1
TEST_2 = 2

# ==========| TEST 1 |==========
def test1():
    fitness = NetworkModel.getFitnessForNetwork(nodeArray)
    print("Fitness: ", fitness)

# ==========| TEST 2 |==========
def test2():
    index = np.random.randint(0, N^2, size=2)
    nodeA = nodeArray[index[0]]
    nodeB = nodeArray[index[1]]
    
    snrTest = NetworkModel.getSNRForLink(nodeA, nodeB)
    
    print("For nodes: A(%s, %s)" %(nodeA.xPos, nodeA.yPos),
          " and B(%s, %s) " %(nodeB.xPos, nodeB.yPos), " - SNR: ", snrTest)
    
# ==========| TEST 3 |==========

def test3():
    
    print(nodeArray[1] is nodeArray[2])

#==========| Test Selection |==========


test1()