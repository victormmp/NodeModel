"""
Test file to analize PreProcess functions
"""

from src.optimization import PreProcess
from src.constants import *
import click
import sys

sys.path.insert(0, r'../')



@click.command('test-line')
@click.option('--nodes', '-n', type=click.INT, required=True, 
               help='Number of nodes of specified line.')
def testLine(nodes):
    nodes = PreProcess.generateNodeListForLine(nodes, N2_DIM)
    x = [node.xPos for node in nodes]
    y = [node.yPos for node in nodes]
    plt.plot(x,y, 'o')
    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    plt.show()


@click.command('test-area')
@click.option('--nodes', '-n', type=click.INT, required=True,
              help='Number of nodes of specified area.')
def testArea(nodes):
    nodes2 = PreProcess.generateNodeListForArea(nodes, N4_DIM)
    x = [node.xPos for node in nodes2]
    y = [node.yPos for node in nodes2]
    plt.plot(x,y, 'o')
    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    plt.show()
