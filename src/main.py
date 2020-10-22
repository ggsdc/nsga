from src.nsga import NondominatedSortingGeneticAlgorithm
from src.problems import Problems

population_size = 15
problem_size = 30

nsga = NondominatedSortingGeneticAlgorithm(population_size, Problems(problem_size, 'zdt1'))
nsga.run()

for i in range(len(nsga.population)):
    print(nsga.population[i].id, nsga.population[i].fitness, nsga.population[i].front,
          nsga.population[i].domination_count, nsga.population[i].dominated_individuals)