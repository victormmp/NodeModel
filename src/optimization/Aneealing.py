"""
Selective Aneealing Alghoritm
"""

from simanneal import Annealer
import random
from src.model.NetNode import Node


class Annealing(Annealer):
    
    def __init__(self, state, step = 1.0):
        """
        :param: state: Node list.
        """
        self.step = step
        super(Annealing, self).__init__(state)

    def move(self):
        """Move a random node within area"""
        node: Node = random.choice(self.state)

        node.xPos = node.xPos + random.uniform(0.0, self.step)
        node.yPos = node.yPos + random.uniform(0.0, self.step)
        
