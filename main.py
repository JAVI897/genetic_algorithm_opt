import time
from utils import Distance, save_config
from schemes import scheme1
import argparse
from parent_selections import parent_selection1, parent_selection2, tournament_selection
from survivor_selections import elitist
from operators import swap, pmx_pair, cim, rsm

parser = argparse.ArgumentParser()

parser.add_argument("--generations", type=int, default=100)
parser.add_argument("--population_size", type=int, default=100)
parser.add_argument("--parent_selection", type=int, default=1)
parser.add_argument("--crossover_selection", type=str, default='pmx')
parser.add_argument("--mutation_selection", type=str, default='swap')
parser.add_argument("--k_tournament", type=int, default=2) # k hyperparameter tournament selection
parser.add_argument("--p_tournament", type=float, default=0.5) # p hyperparameter tournament selection

parser.add_argument("--survivor_selection", type=str, default='elitist') #todo: use names instead of numbers
parser.add_argument("--verbose", type=bool, default=True)
parser.add_argument("--url_locations", type=str, default="https://gitlab.com/drvicsana/opt-proyecto-genetico-2021/-/raw/main/berlin52.tsp")

con = parser.parse_args()

PARENT_SELECTION = con.parent_selection
SURVIVOR_SELECTION = con.survivor_selection
CROSSOVER_SELECTION = con.crossover_selection
MUTATION_SELECTION = con.mutation_selection

config = {'parent_selection': None,
		  'survivor_selection' : None, 
		  'k_tournament': con.k_tournament,
		  'p_tournament': con.p_tournament,
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

if CROSSOVER_SELECTION == 'pmx':
	config['crossover_selection'] = pmx_pair

if MUTATION_SELECTION == 'swap':
	config['mutation_selection'] = swap
elif MUTATION_SELECTION == 'cim':
	config['mutation_selection'] = cim
elif MUTATION_SELECTION == 'rsm':
	config['mutation_selection'] = rsm
	

def main():
	
	distances = Distance(config['url_locations'])
	cities = list(distances.node_locations.keys()) # list of cities
	best_candidate = scheme1(distances, cities, config)
	config['solution'] = best_candidate
	print(best_candidate)

if __name__ == '__main__':
	start = time.time()
	main()
	result_time = time.time() - start
	print("Time result:   {0:.6f}s".format(result_time))
	config['run-time'] = result_time
	save_config(config)