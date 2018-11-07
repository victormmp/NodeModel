"""
Test file to analize PreProcess functions
"""

from src.optimization import PreProcess
from src.model import GlobalParameters as gp
from settings import *
import matplotlib.pyplot as plt
import numpy as np
import click
import sys

sys.path.insert(0, r'../')


@click.command('test-line')
@click.option('--nodes', '-n', type=click.INT, required=True, 
               help='Number of nodes of specified line.')
@click.option('--from-file', is_flag=True)
def testLine(nodes, from_file):

    if from_file:
        gp.loadConstantsFromFile(CONSTANTS_FILE)
        nodeList1 = PreProcess.generateNodeListForLine(nodes, gp.N1_DIM)
        nodeList2 = PreProcess.generateNodeListForLine(nodes, gp.N2_DIM)
        nodeList3 = PreProcess.generateNodeListForLine(nodes, gp.N3_DIM)
        nodeList = np.concatenate((nodeList1, nodeList2, nodeList3))
    else:
        nodeList = PreProcess.generateNodeListForLine(nodes, gp.N1_DIM)

    x = [node.longitude for node in nodeList]
    y = [node.latitude for node in nodeList]
    plt.plot(x,y, 'o')
    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    plt.show()


@click.command('test-area')
@click.option('--nodes', '-n', type=click.INT, required=True,
              help='Number of nodes of specified area.')
@click.option('--from-file', is_flag=True)
def testArea(nodes, from_file):

    if from_file:
        gp.loadConstantsFromFile(CONSTANTS_FILE)
        nodes2 = PreProcess.generateNodeListForArea(nodes, gp.N4_DIM)
    else:
        nodes2 = PreProcess.generateNodeListForArea(nodes, gp.N4_DIM)

    x = [node.longitude for node in nodes2]
    y = [node.latitude for node in nodes2]
    plt.plot(x,y, 'o')
    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    plt.show()

if __name__== '__main__':
    testLine(5, True)