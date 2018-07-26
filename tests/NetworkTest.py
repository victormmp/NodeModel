import NetworkModel
from NetNode import *

N = 7

nodeArray = []

for x in range(N):
    for y in range(N):
        nodeArray.append(Node(x,y))

fitness = NetworkModel.getFitnessForNetwork(nodeArray)

print("Fitness", fitness)


