import matplotlib.pyplot as plt


def plot_node_list(nodes, title=None, xLabel=None, yLabel=None, xLim=None, yLim=None):
    """Plot a node list. Ths list must be a python list() or a numpy.ndarray object."""

    x = [node.xPos for node in nodes]
    y = [node.yPos for node in nodes]

    plt.plot(x,y, 'o')

    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    plt.show()