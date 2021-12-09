import numpy as np

# Crossover 
# --------------------------------------------------------------------------------------

def pmx(parent1, parent2, start, stop, distances):
	child = [None] * len(parent1)
	child[start:stop] = parent1[start:stop]
	
	for ind, x in enumerate(parent2[start:stop]):
		ind += start
		if x not in child:
			while child[ind] != None:
				ind = parent2.index(parent1[ind])
			child[ind] = x

	for ind, x in enumerate(child):
		if x == None:
			child[ind] = parent2[ind]

	return [child, distances.get_distance_of_individual(child), 0]


def pmx_pair(parent1, parent2, distances):
	parent1 = parent1[0]
	parent2 = parent2[0]
	
	half = len(parent1) // 2
	start = np.random.randint(0, len(parent1) - half)
	stop = start + half

	return pmx(parent1, parent2, start, stop, distances), pmx(parent2, parent1, start, stop, distances)


# Mutation
# --------------------------------------------------------------------------------------

def swap(child, distances):
	route = child[0]

	cities = np.random.choice(len(route), 2, replace=False)
	route[cities[0]], route[cities[1]] = route[cities[1]], route[cities[0]]

	return [route, distances.get_distance_of_individual(route), 0]

def cim(child, distances):
	'''
		Centre inverse mutation
		Abdoun, O., & Abouchabaka, J. (2012). A comparative study of adaptive crossover 
		operators for genetic algorithms to resolve the traveling salesman problem. 
		arXiv preprint arXiv:1203.3097.
	'''
	route = child[0]
	i = np.random.choice(len(route), 1)[0]
	route[0:i] = reversed(route[0:i])
	route[i:] = reversed(route[i:])

	return [route, distances.get_distance_of_individual(route), 0]

def rsm(child, distances):
	'''
		Reverse Sequence Mutation
		Abdoun, O., & Abouchabaka, J. (2012). A comparative study of adaptive crossover 
		operators for genetic algorithms to resolve the traveling salesman problem. 
		arXiv preprint arXiv:1203.3097.
	'''
	route = child[0]
	i = np.random.choice(len(route), 1)[0]
	j = np.random.choice(np.arange(i, len(route)), 1)[0]
	route[i:j+1] = reversed(route[i:j+1])

	return [route, distances.get_distance_of_individual(route), 0]