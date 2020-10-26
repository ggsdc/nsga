from src.nsga import NondominatedSortingGeneticAlgorithm
from src.problems import Problems
import matplotlib.pyplot as plt
import pandas as pd

zdt = pd.read_csv("./data/zdt6.csv", header=None)

population_size = 100

nsga = NondominatedSortingGeneticAlgorithm(population_size, Problems('zdt6'), 0.48862, 0.3, 0.01)
nsga.run(2500)
plt.figure()
plt.ylim(0, 4)
first = True
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    if first:
        plt.scatter(i.fitness[0], i.fitness[1], marker='.', color='#000000', label="200 generations")
        first = False
    else:
        plt.scatter(i.fitness[0], i.fitness[1], marker='.', color='#000000')
    plt.plot(zdt[0], zdt[1], color='#FF0000')

nsga.run(200)
# plt.figure()
# plt.ylim(0, 1)
first = True
for i in nsga.population:
    if first:
        plt.scatter(i.fitness[0], i.fitness[1], marker='v', color='#000000', label="400 generations")
        first=False
    else:
        plt.scatter(i.fitness[0], i.fitness[1], marker='v', color='#000000')
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    # plt.plot(zdt[0], zdt[1])

nsga.run(200)
# plt.figure()
# plt.ylim(0, 1)
first = True
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    if first:
        plt.scatter(i.fitness[0], i.fitness[1], marker='s', color='#000000', label="600 generations")
        first = False
    else:
        plt.scatter(i.fitness[0], i.fitness[1], marker='s', color='#000000')
    # plt.plot(zdt[0], zdt[1])

nsga.run(200)
# plt.figure()
# plt.ylim(0, 1)
first = True
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    if first:
        plt.scatter(i.fitness[0], i.fitness[1], marker='D', color='#000000', label="800 generations")
        first = False
    else:
        plt.scatter(i.fitness[0], i.fitness[1], marker='D', color='#000000')
    # plt.plot(zdt[0], zdt[1])

nsga.run(200)
# plt.figure()
# plt.ylim(0, 1)
first = True
for i in nsga.population:
    print(i, i.front, i.fitness, i.parents, i.adjusted_dummy)
    if first:
        plt.scatter(i.fitness[0], i.fitness[1], marker='P', color='#000000', label="1000 generations")
        first = False
    else:
        plt.scatter(i.fitness[0], i.fitness[1], marker='P', color='#000000')
    # plt.plot(zdt[0], zdt[1])

plt.legend(loc='best')
plt.show()