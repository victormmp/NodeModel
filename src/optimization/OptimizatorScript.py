"""
MAIN SCRIPT FLE FOR OPTIMIZATOR
"""

import click
import src.NetworkModel as NetworkModel
import src.model.GlobalParameters as GlobalParameters
import numpy as np
import random
import copy
import logging
from src.utils import LoggerUtils
from src.utils.StopWatch import StopWatch
import src.optimization.OptimizatorService as OptimizatorService

class Constants:
    # Max number of generations
    MAX_GENERATIONS = 1000

    # Mutation probability
    MUTATION_PROB = 0.2

    # Crossover probability
    CROSSOVER_PROBABILITY = 0.7

    # Max number of generations without improve of optimal value
    MAX_STAGNATED_OPTIMAL = 10





@click.command('optimize')
def optimize():
    """
    Optimizator main method. The optimization will be performed using an evolutional
    alghorithm.
    """
    stopwatch = StopWatch()
    logger = LoggerUtils.configure_log(name='Optimization script', use_console=True)

    click.clear()

    metrics = Constants();

    # Generate initial population
    population = OptimizatorService.populate(initial=True)

    # Calculate fitness for each individual and sort them
    ranked_pop = OptimizatorService.adaptability(population)
    
    generation = 0
    same_solution_count = 0
    optimal = {"genome": None, "fitness": None, "links": None}

    logger.info('Starting first optimization loop.')
    # Main loop
    while(generation < metrics.MAX_GENERATIONS and same_solution_count != metrics.MAX_STAGNATED_OPTIMAL):
        generation += 1
        
        # Perform the crossover 
        ranked_pop = OptimizatorService.crossover(ranked_pop, metrics.CROSSOVER_PROBABILITY)

        # Mutate population
        ranked_pop = OptimizatorService.mutate(ranked_pop, metrics.MUTATION_PROB)

        # Next generation
        population = [individual.get('genome') for individual in ranked_pop]

        # Calculate fitness for each individual and sort them
        ranked_pop = OptimizatorService.adaptability(population)

        # Update the optimal value and count improvements
        if optimal.get('fitness') is None:
            optimal = copy.deepcopy(ranked_pop[0])
        elif ranked_pop[0].get('fitness') < optimal.get('fitness'):
            optimal = copy.deepcopy(ranked_pop[0])
            same_solution_count = 0
        else:
            same_solution_count += 1

        # Perform environment pressure
        ranked_pop = OptimizatorService.environment_pressure(ranked_pop)
        
        logger.info(''.join(['[{}] '.format(generation), 'Optimal:{solution: ', str(optimal.get('genome')), ', fitness: ', str(optimal.get('fitness')), 
                        ', min_links: ', str(optimal.get('links')), '}']))
    
    logger.info('Finished fist optimization with %s generations. Total time: %s.' % (generation, stopwatch.read()))
    logger.info('OPTIMAL FOR FIRST OPTIMIZATION: N1: {}, N2: {}, N3: {}, N4: {} '.format(optimal['genome'][0], 
                 optimal['genome'][1], optimal['genome'][2], optimal['genome'][3])
        

        



if __name__ == '__main__':
    optimize()