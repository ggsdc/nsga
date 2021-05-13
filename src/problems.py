from math import sqrt, pow, sin, cos, pi, exp


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


class ZDT2:
    def __init__(self, size):
        self.size = size

    def f1(self, individual):
        return individual.genes[0]

    def f2(self, individual):
        sigma = sum(individual.genes[1:])
        g = 1 + sigma * 9 / (self.size - 1)
        h = 1 - pow((self.f1(individual) / g), 2)
        return g * h


class ZDT3:
    def __init__(self, size):
        self.size = size

    def f1(self, individual):
        return individual.genes[0]

    def f2(self, individual):
        sigma = sum(individual.genes[1:])
        g = 1 + sigma * 9 / (self.size - 1)
        f1 = self.f1(individual)
        h = 1 - sqrt(f1 / g) - (f1 / g) * sin(10 * pi * f1)
        return g * h


class ZDT4:
    def __init__(self, size):
        self.size = size

    def f1(self, individual):
        return individual.genes[0]

    def f2(self, individual):
        sigma = sum([pow(x, 2) - 10 * cos(4 * pi * x) for x in individual.genes[1:]])
        g = 1 + 10 * (self.size - 1) + sigma
        h = 1 - sqrt(self.f1(individual) / g)
        return g * h


class ZDT6:
    def __init__(self, size):
        self.size = size

    def f1(self, individual):
        return 1 - exp(-4 * individual.genes[0]) * pow(
            sin(6 * pi * individual.genes[0]), 6
        )

    def f2(self, individual):
        sigma = sum(individual.genes[1:])
        g = 1 + 9 * pow((sigma / (self.size - 1)), 0.25)
        h = 1 - pow((self.f1(individual) / g), 2)
        return g * h


class Problems:
    def __init__(self, function):
        if function == "zdt1":
            self.function = ZDT1(30)
        elif function == "zdt2":
            self.function = ZDT2(30)
        elif function == "zdt3":
            self.function = ZDT3(30)
        elif function == "zdt4":
            self.function = ZDT4(10)
        elif function == "zdt6":
            self.function = ZDT6(10)
        self.size = self.function.size

    def calculate_fitness(self, individual):
        return [self.function.f1(individual), self.function.f2(individual)]
