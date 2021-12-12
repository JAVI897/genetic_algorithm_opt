import requests
import math
import random
import numpy as np
from matplotlib import pyplot as plt
import os
import json

class Distance:

	def __init__(self, tsp_instance_url):
		self.tsp_instance_url = tsp_instance_url
		self.cached_distances = {}
		self.read_tsp_problem()

	def read_tsp_problem(self):
		self.node_locations = {}
		r = requests.get(self.tsp_instance_url)
		for line in r.text.split('\n')[6:-1]:
			if line == "EOF":
				break
			tokens = line.split()
			edge_number = int(tokens[0])
			position_x = float(tokens[1])
			position_y = float(tokens[2])
			self.node_locations[edge_number] = (position_x, position_y)

	def euclidean_distance(self, x1, y1, x2, y2):
		xd = x1 - x2
		yd = y1 - y2
		distance = round( math.sqrt(xd**2 + yd**2) )
		return distance

	def get_distance(self, node1, node2):
		if node2 < node1:
			node_aux = node1
			node1 = node2
			node2 = node_aux
		distance = None
		if (node1, node2) in self.cached_distances:
			distance = self.cached_distances[(node1,node2)]
		elif node1 in self.node_locations and node2 in self.node_locations:
			(x1, y1) = self.node_locations[node1]
			(x2, y2) = self.node_locations[node2]
			distance = self.euclidean_distance(x1, y1, x2, y2)
			self.cached_distances[(node1, node2)] = distance
		elif node1 in self.node_locations:
			raise Exception("Invalid node location: " + node2)
		elif node2 in self.node_locations:
			raise Exception("Invalid node location: " + node1)
		return distance

	def get_distance_of_individual(self, individual):
		"""Iterates through a tour and sums up all the distances between every city.
		args:
			individual (list): list containing one permutation of citites.
		return:
			final_distance (float): the distance in one particular tour.
		"""
		dist = 0
		for j in range(len(individual) - 1):
			dist += self.get_distance(individual[j], individual[j + 1])
		dist += self.get_distance(individual[0], individual[-1])
		return dist

#Help functions

def calculate_fitness(individual):
	return 1 / individual[1]

def total_distance(population):
	return sum(i[1] for i in population)

def total_fitness(population):
	return sum(i[2] for i in population)


#Population

def create_population(size, cities, distances, seeds):
	population = []
	for i in range(size):
		copy = cities.copy()
		random.seed(seeds[i])
		random.shuffle(copy)
		population.append([copy, distances.get_distance_of_individual(copy), 0]) # ind: ([x], distance, fitness)

	for i in range(len(population)):
		population[i][2] = 1 / population[i][1]
	print(population)
	return population

# calculate metrics during training

def retrieve_info(population, number_of_generations, config):

	max_distance = max(i[1] for i in population)
	min_distance = min(i[1] for i in population)
	mean_distance = np.mean([i[1] for i in population])

	max_fitness = max(i[2] for i in population)
	min_fitness = min(i[2] for i in population)
	mean_fitness = np.mean([i[2] for i in population])

	if config['verbose']:
		print("""Generation: {} \t Max distance: {:.3f} \t Min distance: {:.3f} \t Mean distance: {:.3f} \t Max fitness: {:.9f} Min fitness: {:.9f} \t Mean fitness: {:.9f}""".format(number_of_generations, 
				max_distance, min_distance, mean_distance, max_fitness, min_fitness, mean_fitness))
	return (max_distance, min_distance, mean_distance, max_fitness, min_fitness, mean_fitness)


# update history during training

def update_history(metric_gen:tuple, config):
	config['metrics']['max_distance'].append(metric_gen[0])
	config['metrics']['min_distance'].append(metric_gen[1])
	config['metrics']['mean_distance'].append(metric_gen[2])
	config['metrics']['max_fitness'].append(metric_gen[3])
	config['metrics']['min_fitness'].append(metric_gen[4])
	config['metrics']['mean_fitness'].append(metric_gen[5])

#Plot results

def plot_results_distances(config):
	plt.style.use('seaborn-whitegrid')
	fig = plt.figure(figsize=(15,10))
	n = len(config['metrics']['min_distance'])
	n = range(n)
	plt.plot(n, config['metrics']['min_distance'], '-.', linewidth = 0.8, label = 'Min distance')
	plt.plot(n, config['metrics']['max_distance'], '--', linewidth = 0.8, label = 'Max distance')
	plt.plot(n, config['metrics']['mean_distance'], label = 'Mean distance', color = 'red')
	plt.title('Evolution of max-distance, min-distance, mean-distance')
	plt.xlabel('Generation')
	plt.ylabel('Distance')
	plt.legend()
	plt.show()
	plt.close()

def plot_results_fitness(config):
	plt.style.use('seaborn-whitegrid')
	fig = plt.figure(figsize=(15,10))
	n = len(config['metrics']['min_distance'])
	n = range(n)
	plt.plot(n, config['metrics']['min_fitness'], '-.', linewidth = 0.8, label = 'Min fitness')
	plt.plot(n, config['metrics']['max_fitness'], '--', linewidth = 0.8, label = 'Max fitness')
	plt.plot(n, config['metrics']['mean_fitness'], label = 'Mean fitness', color = 'red')
	plt.title('Evolution of max-fitness, min-fitness, mean-fitness')
	plt.xlabel('Generation')
	plt.ylabel('Fitness')
	plt.legend()
	plt.show()
	plt.close()

# save experiments

def save_config(config):
	config_save = {}
	name_file = ''
	for key, item in config.items():
		if key in ['parent_selection', 'survivor_selection', 'crossover_selection', 'mutation_selection']:
			config_save[key] = item.__name__
			name_file += '{}-{}_'.format(key, item.__name__)
		else:
			config_save[key] = item
			if key in ['population_size', 'generations', 'k_tournament', 'p_tournament']:
				name_file += '{}-{}_'.format(key, item)

	out_path = os.path.join('./save_train_dir/', f'{name_file}.json')
	with open(out_path, 'w') as outfile:
	    json.dump(config_save, outfile)