from math import sqrt


class ZDT1:
    def __init__(self, size):
        self.size = size

    def f1(self, individual):
        return individual.genes[0]

    def f2(self, individual):
        sigma = sum(individual.genes[1:])
        g = 1 + sigma * 9 / (self.size - 1)
        h = 1 - sqrt(self.f1(individual) / g)
        return g * h


class Problems:

    def __init__(self, size, function):
        self.size = size
        if function == 'zdt1':
            self.function = ZDT1(self.size)

    def calculate_fitness(self, individual):
        return [self.function.f1(individual), self.function.f2(individual)]
