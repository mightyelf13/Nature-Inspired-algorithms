import sys
import random
# import matplotlib.pyplot as plt

def read_file(filepath):
    # just a normal function set to import the data drom the files with the data set excatly how specified on the guidliance
    with open(filepath, "r") as f:
        data = f.read().strip().split()

    if not data:
        return 0, 0, []

    n = int(data[0])
    W = int(data[1])
    items = []

    idx = 2
    for _ in range(n):
        val = int(data[idx])
        wt = int(data[idx + 1])
        items.append((val, wt))
        idx += 2

    return n, W, items


def fitness_function(individual, items, capacity):
    """
    Compute the fitness of every individual for the knapsack:
      - individual: is a  list of 0 or 1 bits (selected items):
      - items: list of (value, weight)
      - capacity: max knapsack capacity
    Return 0 if capacity is exceeded.
    """
    total_weight = 0
    total_value = 0

    for gene_index, bit in enumerate(individual):
        if bit == 1:
            val, wt = items[gene_index]
            total_weight += wt
            total_value  += val
            if total_weight > capacity:
                return 0  # invalid, too heavy
    return total_value


def repair_individual(individual, items, capacity):
    """
    Repair each individual that exceeds capacity by randomly removing items
    until it no longer exceeds the capacity.
    """
    total_weight = sum(items[i][1] for i, bit in enumerate(individual) if bit == 1)
    while total_weight > capacity:
        selected_indices = [i for i, bit in enumerate(individual) if bit == 1]
        if not selected_indices:
            break
        remove_idx = random.choice(selected_indices)
        individual[remove_idx] = 0
        total_weight = sum(items[i][1] for i, bit in enumerate(individual) if bit == 1)
    return individual


def tournament_selection(population, fitnesses, tournament_size=3):
    """
    Select one individual from the population using tournament selection.
    """
    competitors = random.sample(range(len(population)), tournament_size)
    best = competitors[0]
    for i in competitors[1:]:
        if fitnesses[i] > fitnesses[best]:
            best = i
    return population[best][:]  


def knapsack(n, W, items, population_size, generations):
    """
    This is like the main function foe rhe genetic algorithm: 
      - We start by creating the initial population
      - Then, run GA steps (selection, crossover, mutation, repair)
      - Of course: return the best solution found
    """
    mutation_rate = 1.0 / n if n else 0.0

    # Creating the initial population
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(n)]
        individual = repair_individual(individual, items, W)
        population.append(individual)

    best_individual = None
    best_fitness = 0
    # List to store the best fitness in each generation
    best_fitness_per_generation = []

    for _ in range(generations):
        # Fitness
        fitnesses = [fitness_function(ch, items, W) for ch in population]

        # Track best for this generation
        generation_best = max(fitnesses)
        generation_best_index = fitnesses.index(generation_best)
        if generation_best > best_fitness:
            best_fitness = generation_best
            best_individual = population[generation_best_index][:]

        # Store the best fitness of this generation
        best_fitness_per_generation.append(generation_best)

        new_population = []
        new_population.append(best_individual[:])  # Elitism: returning some of the best solution so we avoid loosing them
        while len(new_population) < population_size:
            # Selection
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)

            # Crossover: Using 1-point only
            if n > 1 and random.random() < 0.8:
                point = random.randint(1, n - 1)
                child1 = p1[:point] + p2[point:]
                child2 = p2[:point] + p1[point:]
            else:
                child1 = p1[:]
                child2 = p2[:]

            # Mutation
            for i in range(n):
                if random.random() < mutation_rate:
                    child1[i] = 1 - child1[i]
                if random.random() < mutation_rate:
                    child2[i] = 1 - child2[i]

            # Repairing
            child1 = repair_individual(child1, items, W)
            child2 = repair_individual(child2, items, W)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    return best_individual, best_fitness, best_fitness_per_generation


def main():
    # Default values
    population_size = 100
    generations = 200
    # Note: here the code could run on 1 or 2 or 3 argument only issue is that it needs to be ne set order
    if len(sys.argv) > 1:
        filepath = sys.argv[1]              # 1st argument, for file path
        if len(sys.argv) > 2:
            population_size = int(sys.argv[2])  # 2nd argument, for population size
            if len(sys.argv) > 3:
                generations = int(sys.argv[3])      # 3rd argument, for number of generations
    else: 
        filepath = "debug_10.txt" # if, no arugments are passed then we use the default file

    # Read data from file
    n, W, items = read_file(filepath)
    if n == 0:
        print("Error: invalid or empty knapsack file.")
        return
    best_individual, best_value, fitness_history = knapsack(n, W, items, population_size, generations)

    # Print the solution
    print("Best total value:", best_value)
    print("Selected items:", [i for i, bit in enumerate(best_individual) if bit == 1])

    # # Plot the best fitness over generations
    # plt.plot(fitness_history)
    # plt.xlabel("Generation")
    # plt.ylabel("Best Fitness")
    # plt.title("Best Fitness Over Generations")
    # plt.show()

if __name__ == "__main__":
    main()
