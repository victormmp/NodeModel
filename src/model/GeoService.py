from model.NetNode import *
import geojson as gj
import numpy as np

def getCoordinatesForNodes(nodeList):
    
    if type(nodeList) is not np.ndarray:
        if type(nodeList) is list:
            nodeList = np.array(nodeList)
        else:
            raise TypeError("Argument object is not an array, and cannot be processed")
    
    # TODO: Finish this method
    

def getNodesFromGeoJSONFile(file: str):
    """
    Get a list of Node objects with geographic coordinates from a geoJSON file.
    :param file: GeoJSON file path.
    :return: An array of Node objects.
    """
    nodeList: list = []
    with open(file) as f:
        data = gj.load(f)
    
    origin = data.features[0]
    
    for feature in data.features:
        newNode = Node()
        newNode.extractNode(feature.geometry.coordinates, origin.geometry.coordinates)
        nodeList.append(newNode)
    
    return nodeList
    
