import numpy as np

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


def swap_mutate(child, distances):
	route = child[0]

	cities = np.random.choice(len(route), 2, replace=False)
	route[cities[0]], route[cities[1]] = route[cities[1]], route[cities[0]]

	return [route, distances.get_distance_of_individual(route), 0]