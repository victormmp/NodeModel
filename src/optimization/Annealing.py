"""
Selective Aneealing Alghoritm
"""

from simanneal import Annealer
import random
import math
from src.model.NetNode import Node
import src.NetworkModel as NetworkModel
import src.model.LinkService as LinkService


class DistanceAnnealing(Annealer):
    
    def __init__(self, state, boundaries, step = 1.0, minNumberValidLinks = 2):
        """
        :param: state: Node list.
        """
        self.step = step
        self.boundaries = boundaries
        self.minNumberValidLinks = minNumberValidLinks
        super(DistanceAnnealing, self).__init__(state)

    def move(self):
        """Move a random node within area"""

        index = random.choice(range(len(self.state)))
        node: Node = self.state[index]

        node.xPos = random.normalvariate(node.xPos, self.step)
        node.yPos = random.normalvariate(node.yPos, self.step)

        # Truncate positions to maintain node inside limits
        if node.xPos < self.boundaries.get('MIN_X'): node.xPos = self.boundaries.get('MIN_X')
        if node.xPos > self.boundaries.get('MAX_X'): node.xPos = self.boundaries.get('MAX_X')
        if node.yPos < self.boundaries.get('MIN_Y'): node.xPos = self.boundaries.get('MIN_Y')
        if node.yPos > self.boundaries.get('MAX_Y'): node.xPos = self.boundaries.get('MAX_Y')

        self.state[index] = node

    def energy(self):

        fitness = NetworkModel.getFitnessForNetwork(self.state)
        linkList = LinkService.getLinkList(self.state)
        minDist = min([link.distance for link in linkList])

        penalty  = lambda fitness: 1e-16 if fitness.minValidLinks < self.minNumberValidLinks else 1

        # energy = - (minDist * penalty(fitness) )
        energy = - minDist

        return energy


class PositionAnnealing(Annealer):

    MIN_PRR = 0.1

    def __init__(self, state, step=1):

        self.initialPositions = [node.getPoints() for node in state]
        self.step = step
        super(PositionAnnealing, self).__init__(state)
    
    def move(self):
        index = random.choice(range(len(self.state)))
        node: Node = self.state[index]
        nodeInitialPosition = self.initialPositions[index]

        node.xPos = random.normalvariate(node.xPos, self.step)
        node.yPos = random.normalvariate(node.yPos, self.step)

        if self.distance(node.getPoints(), nodeInitialPosition) > self.step:
            node.setPoints(nodeInitialPosition)
        
        self.state[index] = node

    @staticmethod
    def distance(pointA, pointB):
        dist = math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)
        return dist



    def energy(self):
        fitness = NetworkModel.getFitnessForNetwork(self.state)
        linkList = LinkService.getLinkList(self.state)
        # minDist = min([link.distance for link in linkList])

        penalty = lambda fitness: 1e-16 if fitness.minPRR < 0.1 else 1

        energy = - (fitness.minPRR)




        
