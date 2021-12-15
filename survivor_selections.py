#Survivor selection functions

def elitist(population, population_size, config):
	population.sort(key=lambda x: x[2], reverse=True)
	while len(population) > population_size:
		population.pop()

def elitist_with_explicit_fitness_sharing(population, population_size, config):
	beta = config['beta'] # > 1 -- 1.05 
	alpha = config['alpha'] # < 1 -- 0.95
	sigma = config['sigma'] # 5

	def hamming_distance(x, k):
		return sum(1 for i, j in zip(x, k) if i != j)

	def sh(d):
		if d <= sigma:
			return 1 - (d/sigma)**alpha
		return 0

	for i in range(len(population)):
		x, _, f_i = population[i]
		m_i = sum( sh(hamming_distance(x, k)) for k, _, _ in population )
		f_new = (f_i**beta) / (m_i + 0.000001)
		population[i][2] = f_new

	population.sort(key=lambda x: x[2], reverse=True)
	while len(population) > population_size:
		population.pop()
