import random
from math import pow, sqrt
from collections import Counter


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
        self.born = 0
        self.death = 0
        self.parents = []
        self.children = []
        self.mask = []
        self.mutations = []

    def reset_front(self):
        self.front = 0
        self.domination_count = 0
        self.dominated_individuals = []
        self.niche_count = 0
        self.phenotypic_distance = []

    def dominates(self, other_individual):
        first_check = (
            self.fitness[0] <= other_individual.fitness[0]
            and self.fitness[1] <= other_individual.fitness[1]
        )
        second_check = (
            self.fitness[0] < other_individual.fitness[0]
            or self.fitness[1] < other_individual.fitness[1]
        )
        return first_check and second_check

    def mutate(self, mutation_prob):
        while True:
            chance = random.uniform(0, 1)
            if chance <= mutation_prob:
                gene = random.randint(0, len(self.genes) - 1)
                new_value = random.uniform(0, 1)
                self.genes[gene] = new_value
                self.mutations.append((gene, new_value))
            else:
                break

    def __str__(self):
        return "Individual " + str(self.id)

    def __repr__(self):
        return "Individual " + str(self.id)


class NondominatedSortingGeneticAlgorithm:
    """Class to represent the metaheuristic"""

    def __init__(
        self, population_size, problem, sharing_distance, crossover_prob, mutation_prob
    ):
        self.population_size = population_size
        self.population = []
        self.problem = problem
        self.sharing_distance = sharing_distance
        self.max_solution = []
        self.min_solution = []
        self.idx = 1
        self.selected_individuals = []
        self.children = []
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.max_generations = 1
        self.backup_population = []
        self.generation = 1

    def create_initial_population(self):
        for _ in range(self.population_size):
            individual = Individual([], [], self.idx)
            self.idx += 1
            for i in range(self.problem.size):
                individual.genes.append(random.uniform(0, 1))

            individual.fitness = self.problem.calculate_fitness(individual)

            self.population.append(individual)

        self.backup_population += self.population

        for i in range(len(individual.fitness)):
            self.max_solution.append(float("-Inf"))
            self.min_solution.append(float("Inf"))

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
                    for num1, num2, num3, num4 in zip(
                        i.fitness, j.fitness, self.max_solution, self.min_solution
                    ):
                        aux.append(pow((num1 - num2) / (num3 - num4), 2))

                    if sqrt(sum(aux)) < self.sharing_distance:
                        distance = sqrt(sum(aux))
                    else:
                        distance = self.sharing_distance
                    i.phenotypic_distance.append(distance)

                i.niche_count = sum(
                    [
                        1 - distance / self.sharing_distance
                        for distance in i.phenotypic_distance
                    ]
                )
                if i.niche_count < 1:
                    i.niche_count = 1

                i.adjusted_dummy = i.dummy_fitness / i.niche_count

            initial_fitness = (
                min(front_individuals, key=lambda i: i.adjusted_dummy).adjusted_dummy
                * 0.85
            )

            front += 1

    def selection(self):
        self.selected_individuals = []
        for i in self.population:
            self.selected_individuals += [i for _ in range(round(i.adjusted_dummy))]
            unit = random.uniform(0, 1)
            if unit < i.adjusted_dummy % 1:
                self.selected_individuals += [i]

    def crossover(self):
        self.children = []
        while len(self.children) < round(len(self.population)):
            i = random.randint(0, len(self.selected_individuals) - 1)
            first_parent = self.selected_individuals[i]
            second_parent = first_parent
            while first_parent.genes == second_parent.genes:
                j = random.randint(0, len(self.selected_individuals) - 1)
                second_parent = self.selected_individuals[j]

            first_child = Individual([], [], self.idx)
            self.idx += 1
            second_child = Individual([], [], self.idx)
            self.idx += 1

            mask = []

            for i in range(len(first_parent.genes)):
                interval = abs((first_parent.genes[i] - second_parent.genes[i]))
                if first_parent.genes[i] >= second_parent.genes[i]:
                    min_value = second_parent.genes[i] - self.crossover_prob * interval
                    max_value = first_parent.genes[i] + self.crossover_prob * interval
                else:
                    min_value = first_parent.genes[i] - self.crossover_prob * interval
                    max_value = second_parent.genes[i] + self.crossover_prob * interval

                if min_value < 0:
                    min_value = 0
                if max_value > 1:
                    max_value = 1

                mask.append((min_value, max_value))
                first_child.genes.append(random.uniform(min_value, max_value))
                second_child.genes.append(random.uniform(min_value, max_value))

            #
            #
            # for m in range(len(mask)):
            #     value = mask[m]
            #     if value == 0:
            #         first_child.genes.append(first_parent.genes[m])
            #         second_child.genes.append(second_parent.genes[m])
            #     elif value == 1:
            #         first_child.genes.append(second_parent.genes[m])
            #         second_child.genes.append(first_parent.genes[m])

            first_child.parents = [first_parent, second_parent]
            first_child.mask = mask
            second_child.parents = [first_parent, second_parent]
            second_child.mask = mask

            first_child.mutate(self.mutation_prob)
            second_child.mutate(self.mutation_prob)

            first_child.fitness = self.problem.calculate_fitness(first_child)
            second_child.fitness = self.problem.calculate_fitness(second_child)

            self.children.append(first_child)
            self.children.append(second_child)

        self.population += self.children
        self.backup_population += self.children

    def substitution(self):
        new_population = []
        old_population = [i for i in self.population]

        while len(new_population) < self.population_size:
            selected = max(old_population, key=lambda i: i.adjusted_dummy)
            old_population.remove(selected)
            new_population.append(selected)

        self.population = new_population

    def evaluate(self):
        fitness = [i.adjusted_dummy for i in self.population]
        count = Counter(fitness)
        for i in count:
            count[i] = count[i] / len(fitness)
            if count[i] > 0.99:
                print(count)
                print("BREAKS")
                return True
        return False

    def run(self, generations):
        self.max_generations += generations
        if self.generation == 1:
            self.create_initial_population()
            self.check_fitness()
            self.dominated_sort()
            self.calculate_fitness_and_niche()

        while self.generation <= self.max_generations:
            print(self.generation)
            self.selection()
            self.crossover()
            self.check_fitness()
            self.dominated_sort()
            self.calculate_fitness_and_niche()
            # for i in self.population:
            #     print(i, i.fitness, i.front, i.dummy_fitness, i.adjusted_dummy)
            self.substitution()
            # for i in self.population:
            #     print(i, i.fitness, i.front, i.dummy_fitness, i.adjusted_dummy)
            if self.evaluate():
                break
            self.generation += 1

    def next_gen(self):
        self.selection()
        self.crossover()
        self.check_fitness()
        self.dominated_sort()
        self.calculate_fitness_and_niche()
        self.substitution()
        self.generation += 1
