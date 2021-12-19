import random
from utils import total_fitness

def parent_selection1(population, config):
	selected = None
	i = random.randint(0, len(population) - 1)
	while selected == None:
		if i == len(population):
			i = 0

		#Selecting parents based on fitness
		rand = random.uniform(0, 1)
		chance = population[i][2] / total_fitness(population)
		if(rand < chance):
			selected = population[i]
		i += 1

	return selected

def parent_selection2(population, config):
	"""
	Roulette selection
	"""
	selected = None
	tot_fit = total_fitness(population)
	probabilities = [i[2]/tot_fit for i in population]
	i = 0
	while selected == None:
		if i == len(population):
			i = 0
		#Selecting parents based on fitness
		rand = random.uniform(0, 1)
		chance = sum(probabilities[j] for j in range(i))
		if(rand < chance):
			selected = population[i]
		i += 1

	return selected


def tournament_selection(population, config):
	"""
	Tournament selection with repleacement
	"""
	selected = None
	k = config['k_tournament']
	p = config['p_tournament']
	while selected == None:
		indivs = [population[ random.randint(0, len(population) - 1) ] for j in range(k)]
		indivs.sort(key=lambda x: x[2], reverse=True)
		winner = indivs[0]
		rand = random.uniform(0, 1)
		if rand < p:
			selected = winner

	return selected

