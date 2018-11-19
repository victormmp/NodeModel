"""
Selective Aneealing Alghoritm
"""

from simanneal import Annealer
import random
import math
from src.model.NetNode import Node
import src.NetworkModel as NetworkModel
import src.model.LinkService as LinkService
from vincenty import vincenty

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

        # node.xPos = random.normalvariate(node.xPos, self.step)
        # node.yPos = random.normalvariate(node.yPos, self.step)

        # # Truncate positions to maintain node inside limits
        # if node.xPos < self.boundaries.get('MIN_X'): node.xPos = self.boundaries.get('MIN_X')
        # if node.xPos > self.boundaries.get('MAX_X'): node.xPos = self.boundaries.get('MAX_X')
        # if node.yPos < self.boundaries.get('MIN_Y'): node.xPos = self.boundaries.get('MIN_Y')
        # if node.yPos > self.boundaries.get('MAX_Y'): node.xPos = self.boundaries.get('MAX_Y')

        node.longitude = random.normalvariate(node.longitude, self.step)
        node.latitude = random.normalvariate(node.latitude, self.step)

        # Truncate positions to maintain node inside limits
        if node.longitude < self.boundaries.get('MIN_X'): node.longitude = self.boundaries.get('MIN_X')
        if node.longitude > self.boundaries.get('MAX_X'): node.longitude = self.boundaries.get('MAX_X')
        if node.latitude < self.boundaries.get('MIN_Y'): node.latitude = self.boundaries.get('MIN_Y')
        if node.latitude > self.boundaries.get('MAX_Y'): node.latitude = self.boundaries.get('MAX_Y')

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

        # self.initialPositions = [node.getPoints() for node in state]
        self.initialPositions = [node.getCoordinates() for node in state]
        self.step = step
        super(PositionAnnealing, self).__init__(state)
    
    def move(self):
        index = random.randint(0, len(self.state) - 1)
        node: Node = self.state[index]
        currentPosition = node.getCoordinates()
        nodeInitialPosition = self.initialPositions[index]

        nextLon = random.normalvariate(node.longitude, 0.1)
        nextLat = random.normalvariate(node.latitude, 0.1)

        dirr = self.direction(node.getCoordinates(), (nextLat, nextLon))
        nextCoord = self.next_point(node.getCoordinates(), dirr, self.step) 
        node.setLatLon(nextCoord[0], nextCoord[1])

        # if self.distance(node.getCoordinates(), nodeInitialPosition) > self.step:
        if vincenty(node.getCoordinates(), nodeInitialPosition)*1000 > self.step:
            node.setCoordinates(currentPosition, latLon=True)
        
        self.state[index] = node
    
    @staticmethod
    def direction(vector1, vector2):
        module = vincenty(vector1, vector2)*1000
        return [(v2 - v1) / module for v1, v2 in zip(vector1, vector2)]

    @staticmethod
    def next_point(point, direct, length):
        point = [coord + direct_coord * length for coord, direct_coord in zip(point, direct)]
        return point


    def energy(self):
        fitness = NetworkModel.getFitnessForNetwork(self.state)
        # linkList = LinkService.getLinkList(self.state)
        # minDist = min([link.distance for link in linkList])

        # penalty = lambda fitness: 1e-16 if fitness.minPRR < 0.1 else 1

        energy = - (fitness.meanPRR)

        return energy




        
