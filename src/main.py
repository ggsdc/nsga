from src.nsga import NondominatedSortingGeneticAlgorithm
from src.problems import Problems
import matplotlib.pyplot as plt
import pandas as pd

population_size = 100
problem_size = 30

nsga = NondominatedSortingGeneticAlgorithm(population_size, Problems(problem_size, 'zdt1'), 250, 0.48862, 0.01)
nsga.run()
print('\n')
plt.figure()
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    plt.scatter(i.fitness[0], i.fitness[1])

zdt1 = pd.read_csv("./data/zdt1.csv", header=None)
plt.plot(zdt1[0], zdt1[1])