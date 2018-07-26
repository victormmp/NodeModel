# Node class object.
import math
import logging

# logging.basicConfig(filename="src/logs.log")

class Node:

    def __init__(self, xPos=None, yPos=None):
        self.xPos = xPos
        self.yPos = yPos


    def setCoordinates(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


    def setTransmissionParameters(self, pot):
        self.pot = pot


    def getCoordinates(self):
        if hasattr(self, "latitude") and hasattr(self, "longitude"):
            return [self.latitude, self.longitude]
        else:
            raise ValueError("No coordinates configured for the current node.")


    def __sub__(self, other):
        resp = Node(None, None)
        resp.xPos = self.xPos - other.xPos
        resp.yPos = self.yPos - other.yPos

        return resp
    
    
    def __eq__(self, other):
        
        return self.xPos == self.yPos and self.yPos == self.xPos


class Link:
    distance = None


    def __init__(self, nodeA: Node, nodeB: Node):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.distance = self.getDistance()

    def setLQI(self, lqi):
        self.lqi = lqi


    def setRSSI(self, rssi):
        self.rssi = rssi


    def setPRR(self, prr):
        self.prr = prr


    def getDistance(self):
        if self.distance is not None:
            return self.distance
        else:
            dist = math.sqrt((self.nodeA.xPos - self.nodeB.xPos) ** 2 + (self.nodeA.yPos - self.nodeB.yPos) ** 2)
            return dist
