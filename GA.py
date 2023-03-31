# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 07:03:06 2015

@author: GGaregnani, MPrina

NB: pip install -U git+http://github.com/DEAP/deap
constrains not available in the stable version
"""

## 1.1 Types
from deap import base, creator
from termcolor import colored

## 1.2 Initialization
import random
from deap import tools


def GA(bounds, evaluate, weights, n_pop, n_gen, feasible=None, penalty=None):
    """ Excute the GA algorithms.

    :x:  range of variables to create a random grid
    :evaluate: function to evaluate
    :weights: negative minimization, positive maximization
    :n: size of population
    :ngen: number of generations
    :[feasible]: function for boundary constraints
    """

    min_b = list(zip(*bounds))[0]
    max_b = list(zip(*bounds))[1]

    creator.create("FitnessMin", base.Fitness, weights=weights)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    list_attr = []
    for i, bnd in enumerate(bounds):
        attr = 'attr_l%i' % i
        toolbox.register(attr, random.randint, bnd[0], bnd[1])
        list_attr.append(toolbox.__getattribute__(attr))

    toolbox.__dict__.keys()
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     list_attr, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxUniform,
                      indpb=0.5)
    toolbox.register("mutate", tools.mutUniformInt,
                     low=min_b, up=max_b, indpb=1.0/100)                     
#    toolbox.register("mutate", tools.mutPolynomialBounded,
#                     low=min_b, up=max_b, eta=1.0, indpb=1.0/100)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluate)

    if feasible:
        toolbox.decorate("evaluate", tools.DeltaPenality(feasible, penalty))

    pop = toolbox.population(n=n_pop)
    pop0 = pop
    #print(pop)

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    ff0 = fitnesses
    
    for ind, fit in list(zip(pop, fitnesses)):
        ind.fitness.values = fit
    #-------------------------------------define hist with pop0
    ff0 = [ind.fitness.values for ind in pop]
    hist = {'population': {}, 'fitness': {}}
    hist['population'][0] = list(pop0) #list(zip(*pop0))
    hist['fitness'][0] = list(ff0) #list(zip(*ff0))
#    pop_hist=[]
#    fit_hist=[]
#    pop_hist.append(pop0)
#    fit_hist.append(ff0)
    #---------------------------------------

    pop = toolbox.select(pop, len(pop))
    for gen in range(1, n_gen):
        print(gen)
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in list(zip(offspring[::2], offspring[1::2])):
            if random.random() <= 0.9:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        # Evaluate the entire population
        #print(colored(invalid_ind, 'magenta'))
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in list(zip(invalid_ind, fitnesses)):
            ind.fitness.values = fit

        pop = toolbox.select(pop + offspring, n_pop)
        #print(pop)
        
#        pop_hist.append(pop)
        fitnesses = [ind.fitness.values for ind in pop]
#        fit_hist.append(fitnesses)
        #-----------------------------hist for all the others Gen
        hist['population'][gen] = list(pop) #list(zip(*pop))
        fitnesses = [ind.fitness.values for ind in pop]
        hist['fitness'][gen] = list(fitnesses)#list(zip(*fitnesses))

    #ff = map(toolbox.evaluate, pop)
    ff=fitnesses
    
#    history={'populations': pop_hist, 'fitness': fit_hist}

    return pop, ff, hist#(pop0, pop), (ff0, ff), hist
