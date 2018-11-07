import matplotlib.pyplot as plt


def plot_node_list(nodes, title:str=None, xLabel:str=None, yLabel:str=None, xLim:tuple=None, yLim:tuple=None):
    """Plot a node list. Ths list must be a python list() or a numpy.ndarray object."""

    x = [node.longitude for node in nodes]
    y = [node.latitude for node in nodes]

    plt.plot(x,y, 'o')
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.xlim(xLim)
    plt.ylim(yLim)

    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    plt.show()