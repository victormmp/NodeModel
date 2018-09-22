"""
MAIN SCRIPT FLE FOR OPTIMIZATOR
"""

import click
import src.NetworkModel as NetworkModel
import src.model.GlobalParameters as GlobalParameters
import numpy as np
import random
import logging
from src.utils import LoggerUtils
from src.utils.StopWatch import StopWatch
import src.optimization.OptimizatorService as OptimizatorService

class Constants:
    # Max number of generations
    MAX_GENERATIONS = 2

    # Mutation probability
    MUTATION_PROB = 0.1

    # Crossover probability
    CROSSOVER_PROBABILITY = 0.4

    # Max number of generations without improve of optimal value
    MAX_STAGNATED_OPTIMAL = 3



logger = LoggerUtils.configure_log(name='OptimizatorScript', use_console=True)

@click.command('optimize')
def optimize():
    """
    Optimizator main method. The optimization will be performed using an evolutional
    alghorithm.
    """
    stopwatch = StopWatch()

    click.clear()

    metrics = Constants();

    # Generate initial population
    population = OptimizatorService.populate(initial=True)
    
    generation = 0
    same_solution_count = 0
    optimal = None

    logger.info('Starting first optimization loop.')
    # Main loop
    while(generation < metrics.MAX_GENERATIONS or same_solution_count == metrics.MAX_STAGNATED_OPTIMAL):
        generation += 1
    
        # Calculate fitness for each individual and sort them
        ranked_pop = OptimizatorService.adaptability(population)

        # Update the optimal value and count improvements
        if optimal is None: 
            optimal = ranked_pop[0].get('fitness')
        elif ranked_pop[0].get('fitness') < optimal:
            optimal = ranked_pop[0].get('fitness')
            same_solution_count = 0
        else:
            same_solution_count += 1
        
        logger.info(''.join(['Optimal:{solution: ', str(ranked_pop[0].get('individual')), ', fitness: ', str(optimal), 
                        ', mean_links: ', str(ranked_pop[0].get('links')), '}']))
    
    logger.info('Finished execution. Total time: %s.' % stopwatch.read())
        

        



if __name__ == '__main__':
    optimize()