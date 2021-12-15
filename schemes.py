from utils import create_population
from utils import total_distance, total_fitness
import random
import numpy as np
from utils import retrieve_info, plot_results_distances, plot_results_fitness, update_history


#Modify population

def next_generation1(population, distances, config):
	"""
	steady-statemodel
	-----------------
	population_size new childs are generated and replaced 
	according to the survivor_selection strategy
	"""
	population_size = len(population)

	offspring = []
	for i in range(len(population) // 2):

		#Setting parents
		p1 = config['parent_selection'](population, config)
		p2 = config['parent_selection'](population, config)
		
		#Do crossovers
		c1, c2 = config['crossover_selection'](p1, p2, distances)

		#Do mutating 
		c1 = config['mutation_selection'](c1, distances)
		c2 = config['mutation_selection'](c2, distances)

		offspring.append(c1)
		offspring.append(c2)

	for route in offspring:
		route[2] = 1 / route[1]
	
	population += offspring
	
	config['survivor_selection'](population, population_size, config)


#Generation Functions

def generation_generator1(population, distances, config):
	current_best = population[0]
	number_of_generations = 0
	while(number_of_generations < config['generations']):
		next_generation1(population, distances, config)
		number_of_generations += 1
		metric = retrieve_info(population, number_of_generations, config)
		update_history(metric, config)
		
		if(population[0][1] < current_best[1]):
			current_best = population[0]

		if metric[0] == metric[1]: # max_distance == min_distance
			print('Training stopped because max distance == min distance')
			config['generations'] = number_of_generations
			break
		# early stopping after 30 generations. Starts working when generations > 50
		if number_of_generations > 50 and metric[1] == config['metrics']['min_distance'][-30]:
			print('min_distance did not improve after 30 generations. Stopping...')
			config['generations'] = number_of_generations
			break

	if config['verbose']:
		plot_results_distances(config)
		plot_results_fitness(config)

	return current_best

#Schemes

def scheme1(distances, cities, config, seeds):
	population = create_population( config['population_size'], cities, distances, seeds)
	best_candidate = generation_generator1(population, distances, config)
	return best_candidate