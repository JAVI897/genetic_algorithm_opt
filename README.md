# Solving TSP with Genetic Algorithms
### About

The traveling salesman problem (TSP) is a well known NP-hard problem in computer science. Many studies have tried to improve the genetic algorithm used to solve TSP. In this project, several mutation and crossover operators were used for the *berlin52* TSP instance with different selection methods. Some parameters in the genetic algorithm should be adjusted for the algorithm to produce consistent results. In this work, different experiments were performed on the different methods of selection, crossover operators and mutation operators.

### Dependencies

- numpy
- matplotlib

### Usage

You can run the GA with:

```python
python main.py --generations <generations> 
               --population_size <population_size>
               --parent_selection <parent_selection> 
               --crossover_selection <crossover_selection>
               --mutation_selection <mutation_selection>
               --k_tournament <k_tournament> --p_tournament <p_tournament>
               --survivor_selection <survivor_selection>
               --beta <beta> --alpha <alpha> --sigma <sigma>
               --verbose <verbose> --url_locations <url_locations>
```

Specifying the hyperparameters  according to the following table:

| Parameter           | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| **generations**         | Number of generations to perform                             |
| **population_size**     | Number of individuals in the population                      |
| **parent_selection**    | If set to 2, the roulette parent selection is used. If set to 3, the tournament selection is used |
| **crossover_selection** | If set to 'pmx', the partially-mapped *crossover* operator is used. If set to 'COWGC', the Cut on worst gene crossover is used. If set to 'COWLRGC', the Cut On Worst L+R Crossover is used |
| **mutation_selection**  | If set to 'swap', the swap operator is used. If set to 'cim', the centre inverse mutation is used. If set to 'rsm', the reverse sequence mutation is used |
| **k_tournament**        | Number of random individuals to select in one tournament. Only used if parent_selection = 3 |
| **p_tournament**        | Probability of selecting the best individual in the tournament. Only used if parent_selection = 3 |
| **survivor_selection**  | If set to 'elitist', best individuals are chosen based on the fitness metric. If set to 'elitist_fitness_sharing', best individuals are selected after recomputing the fitness for each individual in the population applying fitness sharing |
| **beta**                | beta coefficient used in fitness sharing                     |
| **alpha**               | alpha coefficient used in fitness sharing                    |
| **sigma**               | sigma coefficient used in fitness sharing                    |
| **verbose**             | If set to True, plots and evolution of the algorithm will be shown |
| **url_locations**       | Url of the dataset                                           |

