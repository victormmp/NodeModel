import logging
from LinkService import *
from NetNode import *
from GlobalParameters import  *
import numpy as np

CONFIGURE_LOG = False

    # CONFIGURES LOG OPTIONS
if (CONFIGURE_LOG):
    # create logger with 'spam_application'
    logger = logging.getLogger('NetModel')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('logs/logs.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a debug log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


# Defining number of nodes as N^2
N = 5

# Initialize global Parameters
gp = GlobalParameters()
gp.initialize()

nodeArray = []

for x in range(N):
    for y in range(N):
        nodeArray.append(Node(x,y))

linkList = getLinkList(nodeArray)

meanPRR = getNetworkMeanPRR(linkList)
print("Number of links: ", linkList.size)
print("Mean PRR value: ", meanPRR)
