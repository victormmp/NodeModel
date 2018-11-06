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
        
    def setCoordinates(self, coordinates: list, latLon = False):
        if (latLon):
            self.longitude = coordinates[1]
            self.latitude = coordinates[0]
        else:
            self.longitude = coordinates[0]
            self.latitude = coordinates[1]

    def extractNode(self, coordinates: list, origin, latLon = False):
        self.setCoordinates(coordinates, latLon=latLon)
        if (latLon):
            originPoint: tuple = (origin[0], origin[1])
        else:
            originPoint: tuple = (origin[1], origin[0])
        thisPoint: tuple = self.getCoordinates()
        distanceX = vincenty(originPoint, (originPoint[0], thisPoint[1])) * 1000
        distanceY = vincenty(originPoint, (thisPoint[0], originPoint[1])) * 1000

        posX = distanceX
        posY = distanceY

        if (thisPoint[1] < originPoint[1]): posX = -distanceX
        if (thisPoint[0] < originPoint[0]): posY = -distanceY
        
        self.xPos = posX
        self.yPos = posY
        
    
    def setTransmissionParameters(self, pot):
        self.pot = pot


    def getCoordinates(self):
        if hasattr(self, "latitude") and hasattr(self, "longitude"):
            return (self.latitude, self.longitude)
        else:
            raise ValueError("No coordinates configured for the current node.")

    def getPoints(self):
        if hasattr(self, "xPos") and hasattr(self, "yPos"):
            return (self.xPos, self.yPos)
        else:
            raise ValueError("No points configurated for current node.")
    
    def setPoints(self, points):
        if hasattr(self, "xPos") and hasattr(self, "yPos"):
            self.xPos = points[0]
            self.yPos = points[1]
        else:
            raise ValueError("No points cofigured for current node.")
    
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