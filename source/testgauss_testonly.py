import random
import statistics

MUTATION_FACTOR = 0.1
POP_SIZE = 1000
GENERATIONS = 20000

# initial population
pop = [100.0 for _ in range(POP_SIZE)]

for gen in range(GENERATIONS):
    new_pop = []
    for _ in range(POP_SIZE):
        A = random.choice(pop)
        B = random.choice(pop)
        mean = (A + B) / 2
        child = random.gauss(mean, MUTATION_FACTOR * mean)
        new_pop.append(child)
    pop = new_pop

    if gen % 20 == 0:
        print(gen, statistics.mean(pop), statistics.stdev(pop))