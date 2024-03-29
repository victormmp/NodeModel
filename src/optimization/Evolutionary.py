
import numpy as np
import random
import copy
from src.utils import LoggerUtils
import src.NetworkModel as NetworkModel

logger = LoggerUtils.configure_log(name='Optimizator Services', use_console=True)

class Individual:
    """
    Service class, created to work as static parameter.
    """
    n1 = [7, 8, 9, 10]
    n2 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
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
    MIN_NUMBER_OF_VALID_LINKS = 3

    # Penalty functions
    penalty = lambda links, fitness: (links < MIN_NUMBER_OF_VALID_LINKS) * 1000 + fitness

    for dude in population:
        quality = NetworkModel.getFitnessForVariables(dude[0], dude[1], dude[2], dude[3])
        fitness = penalty(quality.minValidLinks, sum(dude))
        individual = {"genome": dude, "links": quality.minValidLinks, "fitness": fitness}
        ranked_pop.append(individual)
        
    ranked_pop.sort(key=lambda x: x.get('fitness'))
    
    return ranked_pop


def crossover(population: list, prob_crossover, number_childs = None):
    """
    Generate new individuals and perform crossover.
    """

    total_individuals = len(population)

    if number_childs is None:
        number_childs = total_individuals // 3

    genome = Individual()

    new_population = copy.deepcopy(population)

    for _ in range(number_childs):
        parents = [population[index] for index in random.sample(range(total_individuals), 2)]

        # Initialize the child as a perfect copy of one of the parents
        child = copy.deepcopy(parents[0])

        # Perform the cross-over grabbing half of the genome of each parent
        if random.uniform(0.0, 1.0) < prob_crossover:
            half_genomes = len(parents[0]['genome']) // 2
            new_genome = parents[0]['genome'][0:half_genomes] + parents[1]['genome'][half_genomes:]
            child['genome'] = new_genome

        new_population.append(child)
    
    return new_population

            
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


def environment_pressure(population, desired_size = 30):
    """
    Perform environment pressure to get only the best adapted individuals.
    """

    new_population = copy.deepcopy(population[0:desired_size])
    return new_population
