import random


class Individual:
    """Each individual represents a solution to the problem"""
    def __init__(self, genes, fitness, idx):
        self.genes = genes
        self.fitness = fitness
        self.ranking = 0
        self.domination_count = 0
        self.dominated_individuals = []
        self.front = 0
        self.adjusted_fitness = 0
        self.id = idx

    def reset_front(self):
        self.front = 0
        self.domination_count = 0
        self.dominated_individuals = []

    def dominates(self, other_individual):
        first_check = self.fitness[0] <= other_individual.fitness[0] and self.fitness[1] <= other_individual.fitness[1]
        second_check = self.fitness[0] < other_individual.fitness[0] or self.fitness[1] < other_individual.fitness[1]
        return first_check and second_check


class NondominatedSortingGeneticAlgorithm:
    """Class to represent the metaheuristic"""
    def __init__(self, population_size, problem):
        self.population_size = population_size
        self.population = []
        self.problem = problem
        self.idx = 0

    def create_initial_population(self):
        for _ in range(self.population_size):
            individual = Individual([], [], self.idx)
            self.idx += 1
            for i in range(self.problem.size):
                individual.genes.append(random.uniform(0, 1))

            individual.fitness = self.problem.calculate_fitness(individual)

            self.population.append(individual)

    def dominated_sort(self):
        for i in self.population:
            i.reset_front()

        for i in self.population:
            for j in self.population:
                if i.id == j.id:
                    continue

                if i.dominates(j):
                    i.dominated_individuals.append(j.id)
                elif j.dominates(i):
                    i.domination_count += 1

            if i.domination_count == 0:
                i.front = 1

    def selection(self):
        pass

    def crossover(self):
        pass

    def substitution(self):
        pass

    def mutate(self):
        pass

    def run(self):
        self.create_initial_population()
        self.dominated_sort()