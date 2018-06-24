# Node class object.
import math


class Node:

    xPos = None
    yPos = None

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def setCoordinates(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    # def calculateCoordinates(self, originNode):
    #     try:
    #

    def setTransmissionParameters(self, pot):
        self.pot = pot

    def getCoordinates(self):
        return [self.latitude, self.longitude]

    def __sub__(self, other):
        resp = Node(None, None)
        resp.xPos = self.xPos - other.xPos
        resp.yPos = self.yPos - other.yPos

        return resp


class Link:
    distance = None
    rssi = None
    lqi = None
    nodeA = Node()
    nodeB = Node()
    prr = None

    def __init__(self, nodeA, nodeB):
        self.nodeA = nodeA
        self.nodeB = nodeB

    def getLQI(self):
        return self.lqi

    def getRSSI(self):
        return self.rssi

    def getPRR(self):
        return self.prr

    def getDistance(self):
        if self.distance is not None:
            return self.distance

        dist = math.sqrt((self.nodeA.xPos - self.nodeB.xPos) ** 2 + (self.nodeA.yPos - self.nodeB.yPos) ** 2)
        return dist
