from src.nsga import NondominatedSortingGeneticAlgorithm
from src.problems import Problems
import matplotlib.pyplot as plt
import pandas as pd

zdt = pd.read_csv("./data/zdt1.csv", header=None)

population_size = 200

nsga = NondominatedSortingGeneticAlgorithm(population_size, Problems('zdt1'), 0.48862, 0.3, 0.01)
nsga.run(200)
plt.figure()
plt.ylim(0, 1)
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    plt.scatter(i.fitness[0], i.fitness[1])
    plt.plot(zdt[0], zdt[1])

nsga.run(200)
plt.figure()
plt.ylim(0, 1)
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    plt.scatter(i.fitness[0], i.fitness[1])
    plt.plot(zdt[0], zdt[1])

nsga.run(200)
plt.figure()
plt.ylim(0, 1)
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    plt.scatter(i.fitness[0], i.fitness[1])
    plt.plot(zdt[0], zdt[1])

nsga.run(200)
plt.figure()
plt.ylim(0, 1)
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    plt.scatter(i.fitness[0], i.fitness[1])
    plt.plot(zdt[0], zdt[1])

nsga.run(200)
plt.figure()
plt.ylim(0, 1)
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    plt.scatter(i.fitness[0], i.fitness[1])
    plt.plot(zdt[0], zdt[1])
