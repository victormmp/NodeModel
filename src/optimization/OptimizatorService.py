
import numpy as np
import random
import src.NetworkModel as NetworkModel

class Individual:
    """
    Service class, created to work as static parameter.
    """
    n1 = np.array([7, 8, 9, 10], dtype=int)
    n2 = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11], dtype=int)
    n3 = np.array([2, 3, 4, 5, 6, 7,], dtype=int)
    n4 = np.array([5], dtype=int)

    @classmethod
    def get(cls):
        """
        Generate an individual solution, based on genetic algorithm.
        """
        return np.array([random.choice(cls.n1),
                         random.choice(cls.n2),
                         random.choice(cls.n3),
                         random.choice(cls.n4)], dtype=int)


def populate(prev_generation: np.ndarray = None, pop_size = 30, initial: bool = False):
    """
    Generate a population with random individuals, with or without new individuals.
    """

    if initial:

        print('Initial population')

        population = np.zeros([pop_size, 4], dtype=int)

        for subject in range(len(population)):
            population[subject] = Individual.get()

    else:

        if prev_generation is not None and len(prev_generation) > pop_size:
            raise ValueError('The previous generation size is higher than max population size.')
        elif prev_generation is not None:
            population = np.copy(prev_generation)
        
        while len(population) < pop_size:
            population = np.append(population, [Individual.get()], axis=0)

    if len(population) != 30:
        raise ValueError('Wrong population size generated. The method wanted a popultion with \
                          %s individuals but instead get a population with %s individuals.'
                          % (pop_size, population.size))
    
    return population


def adaptability(population: np.ndarray):
    """
    Calculate fitness for each individual of the population. It's like the adaptablity
    of an individual to the surrounding environment.
    """

    # The population ranked by it's adaptability
    ranked_pop = []


    for dude in population:
        fitness = NetworkModel.getFitnessForVariables(dude[0], dude[1], dude[2], dude[3])
        ranked_pop.append({"individual": dude, "links": fitness.meanValidLinks, "fitness": sum(dude)})
    
    ranked_pop.sort(key=lambda x: x.get('fitness'))

    return np.array(ranked_pop)
