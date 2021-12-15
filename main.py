import time
from utils import Distance, save_config
from schemes import scheme1
import argparse
from parent_selections import parent_selection1, parent_selection2, tournament_selection
from survivor_selections import elitist, elitist_with_explicit_fitness_sharing
from operators import COWLRGC, COWGC, pmx_pair, cim, rsm, swap

parser = argparse.ArgumentParser()

parser.add_argument("--generations", type=int, default=100)
parser.add_argument("--population_size", type=int, default=100)
parser.add_argument("--parent_selection", type=int, default=1)
parser.add_argument("--crossover_selection", type=str, default='pmx')
parser.add_argument("--mutation_selection", type=str, default='swap')
parser.add_argument("--k_tournament", type=int, default=2) # k hyperparameter tournament selection
parser.add_argument("--p_tournament", type=float, default=0.5) # p hyperparameter tournament selection

parser.add_argument("--survivor_selection", type=str, default='elitist') #todo: use names instead of numbers
# Hyperparameters for explicit fitness sharing
parser.add_argument("--beta", type=float, default = 1)
parser.add_argument("--alpha", type=float, default = 0)
parser.add_argument("--sigma", type=float, default = 5)

parser.add_argument("--verbose", type=bool, default=False)
parser.add_argument("--url_locations", type=str, default="https://gitlab.com/drvicsana/opt-proyecto-genetico-2021/-/raw/main/berlin52.tsp")
con = parser.parse_args()

def configuration():

	PARENT_SELECTION = con.parent_selection
	SURVIVOR_SELECTION = con.survivor_selection
	CROSSOVER_SELECTION = con.crossover_selection
	MUTATION_SELECTION = con.mutation_selection

	config = {'parent_selection': None,
			  'survivor_selection' : None, 
			  'k_tournament': con.k_tournament,
			  'p_tournament': con.p_tournament,
			  'beta': con.beta,
			  'alpha': con.alpha,
			  'sigma': con.sigma,
			  'generations': con.generations,
			  'population_size': con.population_size,
			  'verbose': con.verbose,
			  'url_locations':con.url_locations,
			  'metrics': {'max_distance':[], 'min_distance':[], 'mean_distance':[], 'max_fitness':[], 'min_fitness':[], 'mean_fitness':[]}
			  }

	if PARENT_SELECTION == 1:
		config['parent_selection'] = parent_selection1
	elif PARENT_SELECTION == 2:
		config['parent_selection'] = parent_selection2
	elif PARENT_SELECTION == 3:
		config['parent_selection'] = tournament_selection


	if SURVIVOR_SELECTION == 'elitist':
		config['survivor_selection'] = elitist
	elif SURVIVOR_SELECTION == 'elitist_fitness_sharing':
		config['survivor_selection'] = elitist_with_explicit_fitness_sharing

	if CROSSOVER_SELECTION == 'pmx':
		config['crossover_selection'] = pmx_pair
	elif CROSSOVER_SELECTION == 'COWGC':
		config['crossover_selection'] = COWGC
	elif CROSSOVER_SELECTION == 'COWLRGC':
		config['crossover_selection'] = COWLRGC

	if MUTATION_SELECTION == 'swap':
		config['mutation_selection'] = swap
	elif MUTATION_SELECTION == 'cim':
		config['mutation_selection'] = cim
	elif MUTATION_SELECTION == 'rsm':
		config['mutation_selection'] = rsm

	return config
	

def main():

	# replicability
	# ------------------------------
	# 5 experiments are done. The mean distance 
	# is computed from the solution of each run

	N = 5
	# seeds to create ALWAYS the same population
	seeds = [list(range(con.population_size*i, con.population_size*i + con.population_size)) for i in range(N)]
	confs = []
	for repetition in range(N):

		seed = seeds[repetition]
		config = configuration()

		distances = Distance(config['url_locations'])
		cities = list(distances.node_locations.keys()) # list of cities

		start = time.time()
		best_candidate = scheme1(distances, cities, config, seed)
		result_time = time.time() - start
		config['solution'] = best_candidate
		config['run-time'] = result_time
		print("Time result:   {0:.6f}s".format(result_time))
		print(best_candidate)

		confs.append(config)

	mean_fitness_exp = sum( c['solution'][2] for c in confs)/N
	mean_distance_exp = sum( c['solution'][1] for c in confs)/N
	# retrieve best experiment
	_, best_run = min(( c['solution'][1], c) for c in confs)
	best_run['mean_distance_experiments'] = mean_distance_exp
	best_run['mean_fitness_experiments'] = mean_fitness_exp
	save_config(best_run)

if __name__ == '__main__':
	main()