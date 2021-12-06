#Survivor selection functions

def elitist(population, population_size):
	population.sort(key=lambda x: x[2], reverse=True)
	while len(population) > population_size:
		population.pop()