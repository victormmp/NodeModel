from src.optimization import PreProcess
from src.optimization.Annealing import DistanceAnnealing, PositionAnnealing
import matplotlib.pyplot as plt
import src.model.GlobalParameters as gp
from settings import *
import click


@click.command('test-distance-annealer')
def test():

    click.clear()
    click.echo('Initiatin test for annealer with a 3x3 grid.')

    gp.loadConstantsFromFile(CONSTANTS_FILE)
    nodes = list(PreProcess.generateNodeListForArea(3, gp.N4_DIM))

    click.echo('Node network generated.')
    plot(nodes)

    # Define area boundaries
    boundaries = dict()
    boundaries['MIN_X'] = gp.N4_DIM.top_left[0]
    boundaries['MAX_X'] = gp.N4_DIM.botom_right[0]
    boundaries['MIN_Y'] = gp.N4_DIM.botom_right[1]
    boundaries['MAX_Y'] = gp.N4_DIM.top_left[1]

    click.echo('Removing two nodes from the list')
    nodes.pop()
    nodes.pop()
    click.echo('Number of nodes in the network: {}'.format(len(nodes)))

    annealer = DistanceAnnealing(nodes, boundaries, step=5)
    annealer.copy_strategy = "slice"

    click.secho('Calibrating annealer', fg='yellow')
    # auto_schedule = annealer.auto(minutes=2)
    # annealer.set_schedule(auto_schedule)

    annealer.Tmax = 16
    annealer.Tmin = 4e-16
    # click.secho('Annealer calibrated. Parameters: {}'. format(auto_schedule), fg='green')

    click.echo('Starting annealer')
    nodes, energy = annealer.anneal()
    click.secho('Annealing completed. Ploting new grid.', fg='green')

    plot(nodes)

def plot(nodes, add=False, color='blue'):
    x = [node.xPos for node in nodes]
    y = [node.yPos for node in nodes]
    plt.plot(x,y, 'o', c=color)
    for x1, y1 in zip(x,y):
        plt.annotate(('%s, %s' %(x1, y1)), xy=(x1, y1))

    if not add :
        plt.show()

@click.command('test-position-annealer')
def testPosition():

    click.clear()
    click.echo('Initiating test for annealer with a 7 node line.')

    gp.loadConstantsFromFile(CONSTANTS_FILE)
    nodes = list(PreProcess.generateNodeListForLine(7, gp.N1_DIM))

    plot(nodes, add=True)

    click.echo('Node network generated.')

    # Define area boundaries
    boundaries = dict()
    boundaries['MIN_X'] = gp.N4_DIM.top_left[0]
    boundaries['MAX_X'] = gp.N4_DIM.botom_right[0]
    boundaries['MIN_Y'] = gp.N4_DIM.botom_right[1]
    boundaries['MAX_Y'] = gp.N4_DIM.top_left[1]

    click.echo('Number of nodes in the network: {}'.format(len(nodes)))

    annealer = PositionAnnealing(nodes, step=2)
    annealer.copy_strategy = "slice"

    click.secho('Calibrating annealer.', fg='yellow')
    auto_schedule = annealer.auto(minutes=2)
    annealer.set_schedule(auto_schedule)

    # annealer.Tmax = 16
    # annealer.Tmin = 4e-16
    # click.secho('Configurating annealer. Tmax: {}, Tmin: {}, Steps: {}'.format(annealer.Tmax, annealer.Tmin, annealer.steps), fg='yellow')
    click.secho('Annealer calibrated. Parameters: {}'. format(auto_schedule), fg='green')

    click.echo('Starting annealer')
    nodes, energy = annealer.anneal()
    click.secho('Annealing completed. Ploting new grid.', fg='green')

    plot(nodes, color='red')

if __name__ == '__main__':
    testPosition()