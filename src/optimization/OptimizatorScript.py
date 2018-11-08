"""
MAIN SCRIPT FILE FOR OPTIMIZATOR
"""

import click
import src.NetworkModel as NetworkModel
import src.model.GlobalParameters as GlobalParameters
import src.optimization.PreProcess as PreProcess
import src.model.LinkService as LinkService
from settings import OUTPUT_PATH
import numpy as np
import scipy.optimize as spOpt
import random
import copy
import logging
import math
from src.utils import LoggerUtils, Plotter, GeoUtils
from src.utils.StopWatch import StopWatch
import src.optimization.Evolutionary as Evolution
from src.optimization.Annealing import DistanceAnnealing, PositionAnnealing

class GeneticAlgorithmConstants:

    # Max number of generations
    MAX_GENERATIONS = 1000

    # Mutation probability
    MUTATION_PROB = 0.5

    # Crossover probability
    CROSSOVER_PROBABILITY = 0.7

    # Max number of generations without improve of optimal value
    MAX_STAGNATED_OPTIMAL = 10


class SelectiveAneelingConstants:

    # Max generations
    MAX_GENERATIONS = 1000

    # Steps
    STEPS = 100000

    # Copy strategy
    COPY_STRATEGY = "slice"

    # Initial temperature
    TMAX = 20

    # Final temperature
    TMIN = 0.1



@click.command('optimize')
def optimize():
    """
    Optimizator main method. The optimization will be performed using an evolutional
    alghorithm.
    """
    stopwatch = StopWatch()

    ANNEAL_AREA = False
    logger = LoggerUtils.configure_log(name='Optimization script', use_console=True, use_file=True)

    click.clear()

    metrics = GeneticAlgorithmConstants();

    # Generate initial population
    population = Evolution.populate(initial=True)

    # Calculate fitness for each individual and sort them
    ranked_pop = Evolution.adaptability(population)
    
    generation = 0
    same_solution_count = 0
    optimal = {"genome": None, "fitness": None, "links": None}

    logger.info('Starting first optimization loop.')
    # The first optimization loop defines the number of nodes for each of the line instalation areas, 
    # while keeping squared areas number of nodes constant

    # Main loop for the first optimization
    while(generation < metrics.MAX_GENERATIONS and same_solution_count != metrics.MAX_STAGNATED_OPTIMAL):
        generation += 1
        
        # Perform the crossover 
        ranked_pop = Evolution.crossover(ranked_pop, metrics.CROSSOVER_PROBABILITY)

        # Mutate population
        ranked_pop = Evolution.mutate(ranked_pop, metrics.MUTATION_PROB)

        # Next generation
        population = [individual.get('genome') for individual in ranked_pop]

        # Calculate fitness for each individual and sort them
        ranked_pop = Evolution.adaptability(population)

        # Update the optimal value and count improvements
        if optimal.get('fitness') is None:
            optimal = copy.deepcopy(ranked_pop[0])
        elif ranked_pop[0].get('fitness') < optimal.get('fitness'):
            optimal = copy.deepcopy(ranked_pop[0])
            same_solution_count = 0
        else:
            same_solution_count += 1

        # Perform environment pressure
        ranked_pop = Evolution.environment_pressure(ranked_pop)
        
        logger.info(''.join(['[Gen {}] '.format(generation), 'Optimal:{solution: ', str(optimal.get('genome')), ', fitness: ', str(optimal.get('fitness')), 
                        ', min_links: ', str(optimal.get('links')), '}']))
    
    logger.info('Finished first optimization with %s generations. Total time: %s.' % (generation, stopwatch.read()))
    logger.info('OPTIMAL FOR FIRST OPTIMIZATION: N1: {}, N2: {}, N3: {}, N4: {} '.format(optimal['genome'][0], 
                 optimal['genome'][1], optimal['genome'][2], optimal['genome'][3]))
        
    # SECOND OPTIMIZATION ROUTINE:
    # Voronoi : generate optimized points distribution in an area.
    # L-BFGS-B : 
    # POSSIBILITY: Model the second optimization problem as max f(x) = min SUM distances(i,j) 

    # GETTING READY FOR SECOND OPTIMIZATION

    n1, n2, n3, n4 = optimal['genome']
    # network = PreProcess.generateNetworkForConstants(n1, n2, n3, n4)
    fitness = NetworkModel.getFitnessForVariables(n1, n2, n3, n4)

    area_nodes = n4
    generation = 0

    logger.info('Starting second optimization.')
    # The second optimization cares to find the min number of nodes within squared areas. At this part of the code
    # it's assumed that the min number of nodes for the line areas are known due the first optimization loop.

    logger.info('Initial genome [N1 = {}, N2 = {}, N3 = {}, N4 = {}].'. format(n1, n2, n3, n4))
    stopwatch_loop_2 = StopWatch()


    network = PreProcess.generateNetworkForConstants(n1, n2, n3, n4) 
    lines = ['N1', 'N2', 'N3', 'N4']
    nodeArray = [network.get('SINK')]
    for line in lines:
        nodeArray += list(network.get(line))
    # Plotter.plot_node_list(nodeArray, title='First Optimization Result', xLabel='Grid Coordinate (m)', yLabel='Grid Coordinate (m)')

    nodesCoordinates = [node.getCoordinates() for node in nodeArray]
    GeoUtils.writeGeoJSON(nodesCoordinates, OUTPUT_PATH + 'first.geojson')

    # Main loop for the second optimization
    while generation < metrics.MAX_GENERATIONS and fitness.minValidLinks >= 3:
        # First find the min number n of nodes of node at each side of the nxn grid
        
        generation += 1
        area_nodes -= 1

        if area_nodes == 0:
            break

        fitness = NetworkModel.getFitnessForVariables(n1, n2, n3, area_nodes)

        logger.info('[Gen {}] Fitness for N4 = {}: {}'.format(generation, area_nodes, fitness))

    # When the loop ends, area_nodes have a number with invalid fitness for n4.
    # So the correct min number is the result area_nodes + 1.
    n4 = area_nodes + 1
    fitness = NetworkModel.getFitnessForVariables(n1, n2, n3, n4)

    logger.info('Finished second optimization with %s generations. Total time: %s.' % (generation, stopwatch_loop_2.read()))
    logger.info('Optimal for second optimization: N1: {}, N2: {}, N3: {}, N4: {} '.format(n1, n2, n3, n4))
    logger.info('Fitness for second optimization: {}'.format(fitness))

    # Retrieve network 
    network = PreProcess.generateNetworkForConstants(n1, n2, n3, n4)

    metrics = SelectiveAneelingConstants()

    networkArea = list(network.get('N4'))
    current_optimal_network_area = networkArea    

    if len(networkArea) >= 2 :
        fitness = NetworkModel.getFitnessForNetwork(networkArea)
    generation = 1

    # Define area boundaries
    boundaries = dict()
    boundaries['MIN_X'] = GlobalParameters.N4_DIM.top_left[0]
    boundaries['MAX_X'] = GlobalParameters.N4_DIM.botom_right[0]
    boundaries['MIN_Y'] = GlobalParameters.N4_DIM.botom_right[1]
    boundaries['MAX_Y'] = GlobalParameters.N4_DIM.top_left[1]

    if ANNEAL_AREA: logger.info('Starting third optimization. Selective aneeling')

    # Finds the optimal number of nodes within area maximizing the distance between them
    while generation < metrics.MAX_GENERATIONS and fitness.minValidLinks >= 2 and len(networkArea) >= 2 and ANNEAL_AREA:

        current_optimal_network_area = networkArea
        networkArea.pop()

        # Configuring Annealer
        annealer = DistanceAnnealing(networkArea, boundaries)
        annealer.copy_strategy = metrics.COPY_STRATEGY

        # Calibrating Annealer
        click.secho('Calibrating annealer', fg='yellow')
        auto_schedule = annealer.auto(minutes=1)
        annealer.set_schedule(auto_schedule)
        click.secho('Annealer calibrated! Parameters: {}'.format(auto_schedule), fg='green')

        networkArea, energy = annealer.anneal()
        
        fitness = NetworkModel.getFitnessForNetwork(networkArea)

        logger.info("[GEN {}] Number of Links: {}  Energy: {}, fitness: {}".format(len(networkArea), generation, energy, fitness))

        generation += 1
        
    
    logger.info('Finished second optimization. Nodes positions inside area defined. {} nodes installed.'.format(len(current_optimal_network_area)))

    # Saving the new area node disposition
    network['N4'] = np.array(current_optimal_network_area)

    # Adding all nodes of the network in one array

    lines = ['N1', 'N2', 'N3', 'N4']
    nodeArray = [network.get('SINK')]

    for line in lines:
        nodeArray += list(network.get(line))
    
    Plotter.plot_node_list(nodeArray, add=True, annotate=False, label='Posições sem ajuste')
    nodesCoordinates = [node.getCoordinates() for node in nodeArray]
    GeoUtils.writeGeoJSON(nodesCoordinates, OUTPUT_PATH + 'second.geojson')
    
    logger.info('Annealing nodes. Current configuration have %s nodes.' %(len(nodeArray)))
    annealer = PositionAnnealing(nodeArray)
    annealer.copy_strategy = metrics.COPY_STRATEGY

    # click.secho('Calibrating annealer.', fg='yellow')

    # auto_schedule = annealer.auto(minutes=1)
    # annealer.set_schedule(auto_schedule)

    # click.secho('Annealer calibrated!', fg='green')
    # logger.info('Annealer parameters: {}'.format(auto_schedule))

    annealer.Tmax=1.5
    annealer.Tmin=1e-10

    nodeArray, energy = annealer.anneal()

    network[line] = nodeArray
    
    click.secho('Finished Optimization', fg='green')
    logger.info('Finished network optimization. Total elapsed time: {}'.format(stopwatch.read()))
    logger.info('Writing result geoJSON at {}.'.format(OUTPUT_PATH))

    nodesCoordinates = [node.getCoordinates() for node in nodeArray]
    GeoUtils.writeGeoJSON(nodesCoordinates, OUTPUT_PATH + 'result.geojson')

    Plotter.plot_node_list(nodeArray, title='Final Network Layout', xLabel='Grid Coordinate (m)', yLabel='Grid Coordinate (m)',
                            color='red', annotate=False, label='Posições ajustadas')


if __name__ == '__main__':
    optimize()