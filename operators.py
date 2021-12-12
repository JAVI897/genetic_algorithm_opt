import numpy as np

# Crossover 
# --------------------------------------------------------------------------------------

def COWGC(parent1, parent2, distances):
	'''
		Cut on worst gene crossover (COWGC)
		Alkafaween, E. A. O. (2018). Novel methods for 
		enhancing the performance of genetic algorithms. 
		arXiv preprint arXiv:1801.02827.
	'''
	parent1 = parent1[0]
	parent2 = parent2[0]

	distance1, cut_point1 = max([( distances.get_distance(parent1[i], parent1[i+1]), i) for i in range(len(parent1) - 1)] + [( distances.get_distance(parent1[0], parent1[-1]), len(parent1) - 1)])
	distance2, cut_point2 = max([( distances.get_distance(parent2[i], parent2[i+1]), i) for i in range(len(parent2) - 1)] + [( distances.get_distance(parent2[0], parent2[-1]), len(parent2) - 1)])

	if distance1 > distance2:
		child1, child2 = modified_crossover_COWGC(parent1, parent2,cut_point1)
	else:
		child1, child2 = modified_crossover_COWGC(parent1, parent2, cut_point2)

	return [child1, distances.get_distance_of_individual(child1), 0], [child2, distances.get_distance_of_individual(child2), 0]

def modified_crossover_COWGC(parent1, parent2, cut_point):
	'''
		Modified crossover
		Davis, L. (1985, August). Applying adaptive 
		algorithms to epistatic domains. 
		In IJCAI (Vol. 85, pp. 162-164).
	'''
	before_cutoff_p1 = parent1[:cut_point]
	before_cutoff_p2 = parent2[:cut_point]

	for i in parent2:
		if i not in before_cutoff_p1:
			before_cutoff_p1.append(i)

	for i in parent1:
		if i not in before_cutoff_p2:
			before_cutoff_p2.append(i)

	return before_cutoff_p1, before_cutoff_p2

def pmx(parent1, parent2, start, stop, distances):
	child = [None for i in range( len(parent1))]
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