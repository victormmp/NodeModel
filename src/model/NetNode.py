"""
This method contains all network root objects.

CLASS:

1 - NODE:       Node object model. It's equivalent to a radio installed.

2 - LINK:       Link object. It contains all information about a link between two nodes,
                such as transmission quality parameters, distance, etc.

"""
import math
from vincenty import vincenty
import numpy as np

class Node:

    def __init__(self, xPos=None, yPos=None):
        self.xPos = xPos
        self.yPos = yPos

    def setLatLon(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
    def setCoordinates(self, coordinates: list):
        self.longitude = coordinates[0]
        self.latitude = coordinates[1]

    def extractNode(self, coordinates: list, origin):
        self.setCoordinates(coordinates)
        originPoint: tuple = (origin[1], origin[0])
        thisPoint: tuple = self.getCoordinates()
        distanceX = vincenty(originPoint, (originPoint[0], thisPoint[1])) * 1000
        distanceY = vincenty(originPoint, (thisPoint[0], originPoint[1])) * 1000
        
        self.xPos = distanceX
        self.yPos = distanceY
        
    
    def setTransmissionParameters(self, pot):
        self.pot = pot


    def getCoordinates(self):
        if hasattr(self, "latitude") and hasattr(self, "longitude"):
            return (self.latitude, self.longitude)
        else:
            raise ValueError("No coordinates configured for the current node.")
    

    def __sub__(self, other):
        resp = Node(None, None)
        resp.xPos = self.xPos - other.xPos
        resp.yPos = self.yPos - other.yPos

        return resp
    
    
    def __eq__(self, other):
        
        equalPoints = self.xPos == other.xPos and self.yPos == other.yPos
        equalCoordinates = self.latitude == other.latitude and self.longitude == other.longitude
        
        return equalCoordinates or equalPoints


class Link:
    distance = None
    nodeA: Node = None
    nodeB: Node = None


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


    def getDistanceFromPoints(self):
        if self.distance is not None:
            return self.distance
        else:
            dist = math.sqrt((self.nodeA.xPos - self.nodeB.xPos) ** 2 + (self.nodeA.yPos - self.nodeB.yPos) ** 2)
            return dist
        
    
    def getDistanceFromCoordinates(self):
        value = vincenty(self.nodeA.getCoordinates(), self.nodeB.getCoordinates())
        if value is not None:
            return value * 1000
        else:
            raise ValueError("Failed get distance from coordinates.")
    
    def getDistance(self):
        try:
            return self.getDistanceFromCoordinates()
        except:
            return self.getDistanceFromPoints()