import matplotlib.pyplot as plt


def plot_node_list(nodes, title:str=None, xLabel:str=None, yLabel:str=None, xLim:tuple=None, yLim:tuple=None, annotate=True,
                   add=False, color='blue', label=None):
    """Plot a node list. Ths list must be a python list() or a numpy.ndarray object."""

    x = [node.longitude for node in nodes]
    y = [node.latitude for node in nodes]

    plt.plot(x,y, 'o', c=color)
    if title is not None: plt.title(title)
    if xLabel is not None: plt.xlabel(xLabel)
    if yLabel is not None: plt.ylabel(yLabel)
    if xLim is not None: plt.xlim(xLim)
    if yLim is not None: plt.ylim(yLim)
    if label is not None: plt.legend([label])

    if annotate:
        for x1, y1 in zip(x,y):
            plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    if not add:
        plt.show()