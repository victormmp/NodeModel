
import numpy as np
import random
from src.utils import LoggerUtils
import src.NetworkModel as NetworkModel

logger = LoggerUtils.configure_log(name='Optimizator Services', use_console=True)

class Individual:
    """
    Service class, created to work as static parameter.
    """
    n1 = [7, 8, 9, 10]
    n2 = [3, 4, 5, 6, 7, 8, 9, 10, 11]
    n3 = [2, 3, 4, 5, 6, 7]
    n4 = [5]

    @classmethod
    def get(cls):
        """
        Generate an individual solution, based on genetic algorithm.
        """
        return [random.choice(cls.n1),
                random.choice(cls.n2),
                random.choice(cls.n3),
                random.choice(cls.n4)]
    
    def random_cromossome(self, cromossome):
        return {1: random.choice(self.n1),
                2: random.choice(self.n2),
                3: random.choice(self.n3),
                4: random.choice(self.n4)}.get(cromossome)
     


def populate(prev_generation: list = None, pop_size = 30, initial: bool = False):
    """
    Generate a population with random individuals, with or without new individuals.
    """

    if initial:

        logger.info('Creating initial random population with %s individuals.' % pop_size)

        population = []

        for subject in range(pop_size):
            population.append(Individual.get())

    else:

        if prev_generation is not None and len(prev_generation) > pop_size:
            raise ValueError('The previous generation size is higher than max population size.')
        elif prev_generation is not None:
            population = prev_generation.copy()
        
        while len(population) < pop_size:
            population.append(Individual.get())

    if len(population) != 30:
        raise ValueError('Wrong population size generated. The method wanted a popultion with %s individuals but instead get a population with %s individuals.'
                          % (pop_size, len(population)))
    
    return population


def adaptability(population: list):
    """
    Calculate fitness for each individual of the population. It's like the adaptablity
    of an individual to the surrounding environment.
    """

    # The population ranked by it's adaptability
    ranked_pop = []

    # Constraints
    MIN_NUMBER_OF_VALID_LINKS = 2

    # Penalty functions
    penalty = lambda links, fitness: (links < MIN_NUMBER_OF_VALID_LINKS) * 1000 + fitness

    for dude in population:
        quality = NetworkModel.getFitnessForVariables(dude[0], dude[1], dude[2], dude[3])
        fitness = penalty(quality.minValidLinks, sum(dude))
        individual = {"genome": dude, "links": quality.minValidLinks, "fitness": fitness}
        ranked_pop.append(individual)
        
    ranked_pop.sort(key=lambda x: x.get('fitness'))
    
    return ranked_pop


def procriate(population: list, prob_crossover):
    """
    Generate new individuals and perform crossover.
    """


def mutate(population: list, prob_mutation):
    """
    Mutate individuals of the population based on mutation probability.
    """
    genome = Individual()

    for individual in population:
        if (random.uniform(0.0, 1.0) < prob_mutation):
            cromossome = random.choice([1,2,3])
            individual['genome'][cromossome - 1] = genome.random_cromossome(cromossome)
    
    return population