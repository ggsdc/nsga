import random
from math import pow, sqrt

class Individual:
    """Each individual represents a solution to the problem"""
    def __init__(self, genes, fitness, idx):
        self.genes = genes
        self.fitness = fitness
        self.dummy_fitness = 0
        self.adjusted_dummy = 0
        self.phenotypic_distance = []
        self.niche_count = 0
        self.ranking = 0
        self.domination_count = 0
        self.dominated_individuals = []
        self.front = 0

        self.id = idx

    def reset_front(self):
        self.front = 0
        self.domination_count = 0
        self.dominated_individuals = []
        self.niche_count = 0
        self.phenotypic_distance = []

    def dominates(self, other_individual):
        first_check = self.fitness[0] <= other_individual.fitness[0] and self.fitness[1] <= other_individual.fitness[1]
        second_check = self.fitness[0] < other_individual.fitness[0] or self.fitness[1] < other_individual.fitness[1]
        return first_check and second_check

    def __str__(self):
        return 'Individual ' + str(self.id)

    def __repr__(self):
        return 'Individual ' + str(self.id)


class NondominatedSortingGeneticAlgorithm:
    """Class to represent the metaheuristic"""
    def __init__(self, population_size, problem, sharing_distance):
        self.population_size = population_size
        self.population = []
        self.problem = problem
        self.sharing_distance = sharing_distance
        self.max_solution = []
        self.min_solution = []
        self.idx = 0

    def create_initial_population(self):
        for _ in range(self.population_size):
            individual = Individual([], [], self.idx)
            self.idx += 1
            for i in range(self.problem.size):
                individual.genes.append(random.uniform(0, 1))

            individual.fitness = self.problem.calculate_fitness(individual)

            self.population.append(individual)

        for i in range(len(individual.fitness)):
            self.max_solution.append(float('-Inf'))
            self.min_solution.append(float('Inf'))

    def check_fitness(self):

        for j in range(len(self.population[0].fitness)):
            selected_max = max(self.population, key=lambda i: i.fitness[j])
            selected_min = min(self.population, key=lambda i: i.fitness[j])
            if selected_max.fitness[j] >= self.max_solution[j]:
                self.max_solution[j] = selected_max.fitness[j]
            if selected_min.fitness[j] <= self.min_solution[j]:
                self.min_solution[j] = selected_min.fitness[j]

    def dominated_sort(self):
        front = 1
        for i in self.population:
            i.reset_front()

        for i in self.population:
            for j in self.population:
                if i.id == j.id:
                    continue

                if i.dominates(j):
                    i.dominated_individuals.append(j)
                elif j.dominates(i):
                    i.domination_count += 1

            if i.domination_count == 0:
                i.front = front

        while True:
            temp = [i for i in self.population if i.front == 0]
            current_front = [i for i in self.population if i.front == front]
            front += 1
            for ind in current_front:
                for other_ind in ind.dominated_individuals:
                    other_ind.domination_count -= 1
                    if other_ind.domination_count == 0:
                        other_ind.front = front
                        temp.pop(temp.index(other_ind))

            if len(temp) == 0:
                break

    def calculate_fitness_and_niche(self):
        front = 1
        initial_fitness = 100
        while True:
            front_individuals = [i for i in self.population if i.front == front]
            if len(front_individuals) == 0:
                break
            for i in front_individuals:
                i.dummy_fitness = initial_fitness
                for j in front_individuals:
                    if i == j:
                        continue

                    aux = []
                    for num1, num2, num3, num4 in zip(i.fitness, j.fitness, self.max_solution, self.min_solution):
                        aux.append(pow((num1 - num2) / (num3 - num4), 2))

                    if sqrt(sum(aux)) < self.sharing_distance:
                        distance = sqrt(sum(aux))
                    else:
                        distance = self.sharing_distance
                    i.phenotypic_distance.append(distance)

                i.niche_count = sum([1 - distance / self.sharing_distance for distance in i.phenotypic_distance])
                if i.niche_count < 1:
                    i.niche_count = 1

                i.adjusted_dummy = i.dummy_fitness / i.niche_count

            initial_fitness = min(front_individuals, key=lambda i: i.adjusted_dummy).adjusted_dummy*0.9

            front += 1

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
        self.check_fitness()
        self.dominated_sort()
        self.calculate_fitness_and_niche()