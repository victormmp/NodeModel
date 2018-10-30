"""
Selective Aneealing Alghoritm
"""

from simanneal import Annealer
import random
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

        node.xPos = node.xPos + random.uniform(0.0, self.step)
        node.yPos = node.yPos + random.uniform(0.0, self.step)

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

        energy = 1 / (minDist * penalty(fitness) )

        return energy



        
