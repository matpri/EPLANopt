# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:30:37 2015

@author: MPrina
Genetic Algorith implemented with deap algorith

version 1.1 to install from master branch of github repository
pip install -U git+http://github.com/DEAP/deap
"""
from GA import GA
from libeplan import Node
from termcolor import colored
import time

global VARIABLES, START, X, MOLT_FACTORS, INPUTFILE
global ENERGYPLAN, OUT_FOLDER, FUNCTION_2_EVAL
global CONSTRAIN

#------------------------------------INPUT DATA--------------------------------

data = {"EnergyPLAN folder": r"C:\Users\MPrina\Desktop\ZipEnergyPLAN161",
        "Input file": r"C:\Users\MPrina\Desktop\INEST PNRR\EPLANopt-main (2)\EPLANopt-main\INPUT\Denmark2030Reference_ANSI.txt",
        "Output folder": r"C:\Users\MPrina\Desktop\INEST PNRR\EPLANopt-main (2)\EPLANopt-main\OUTPUT",
        "Number of process": 1,
        "Genetic algorithm": {"Size of population": 4,
                               "Number of generations": 1},

        "Variables": [{"EnergyPLAN Name": "input_RES1_capacity", "Range": [17, 100],"Moltiplication factor": 10}, #[10, 50]
                      {"EnergyPLAN Name": 'input_cap_pp_el', "Range": [0, 10],"Moltiplication factor": 10}, #[0, 1]
                      {"EnergyPLAN Name": 'input_storage_pump_cap', "Range": [0, 100],"Moltiplication factor": 10}] #[0, 75]
        }
        
#------------------------------------INITIALIZING------------------------------
VARIABLES = tuple([dic['EnergyPLAN Name'] for dic in data["Variables"]])

X = [tuple(dic['Range']) for dic in data["Variables"]]
MOLT_FACTORS = [dic['Moltiplication factor'] for dic in data["Variables"]]
NPOP= data['Genetic algorithm']["Size of population"]
NGEN= data["Genetic algorithm"]["Number of generations"]

INPUTFILE = data["Input file"]
ENERGYPLAN = data["EnergyPLAN folder"]
OUT_FOLDER = data["Output folder"]
#--------------------------------------
collection={}
c=[]
b=[]



def f(individual):
    print('------------------------------------')
    INPUTFILE = data["Input file"]
    ENERGYPLAN = data["EnergyPLAN folder"]
    OUT_FOLDER = data["Output folder"]

    START = Node(INPUTFILE, ENERGYPLAN, OUT_FOLDER)
    new_data = START.data
    varEP = [i*j for i,j in list(zip(MOLT_FACTORS, individual))]
    
    for i, key in enumerate(VARIABLES):
        new_data[key] = varEP[i]

    INPUTFILE = INPUTFILE.replace('.txt','new_node'+'.txt')
    out_file = r'%s\output.txt' % (OUT_FOLDER)

    new_node = Node(INPUTFILE, ENERGYPLAN, out_file, new_data)

    name_ind='_'.join(map(str, individual))
    print (colored(name_ind, 'blue'))

    if name_ind in collection:
        b.append(1)
        print (colored('a simulation saved, n = %d' %len(b), 'red'))
        dic = collection[name_ind]
        #print (len(collection))             
    else:
        new_node.write_input()
        new_node.excute()
#        print(new_node)
        dic = new_node.read_output_y()
        c.append(1)
        print('a simulation executed, n = %d' %len(c))
        collection[name_ind] = dic #new_node
    
#------------------------------------------------------------------------------
    
    Costs = dic['TOTAL ANNUAL COSTS'] # [M€] non manca un per mille perche è vero che sono GWh ma poi si ottengono k€ 

    CO2 = dic['CO2-emission (total)'] # CO2 [kt]
    
    #CEEP= dic['CO2-emission (total)']
    print('Costs:', colored(Costs, 'red'), '[M€]')
    print('CO2:', colored(CO2, 'green'), '[kt]')
    #print('CEEP:', colored(CEEP, 'blue'), '[kt]')
    return CO2, Costs
    
objectives = (-1.0, -1.0)
pop, ff, hist = GA(X, f, objectives, NPOP, NGEN)
#if __name__ == "__main__":
t0 = time.time()
#pop, ff, hist = testEP()

print ('...............................................')

#-----------------------SAVE RESULTS ON A .csv---------------------------------
hist_file = open('history_csv.csv', 'w')
for i in range(len(VARIABLES)):
    hist_file.write(str(VARIABLES[i]) + ',')
hist_file.write('CO2 emissions [kt]'+ ',')
hist_file.write('Total annual costs [keuro]'+ ',')
# hist_file.write('CEEP [TWh]'+ ',')
hist_file.write('\n')
for a in range(len(hist['population'])):
    for b in range(len(hist['population'][0])):
        for c in range(len(hist['population'][0][0])):
            hist_file.write(str(hist['population'][a][b][c]*MOLT_FACTORS[c]) + ',')
        # Write fitness data
        fitness_data = [str(hist['fitness'][a][b][d]) for d in range(len(hist['fitness'][0][0]))]
        hist_file.write(','.join(fitness_data))  # Join fitness data without trailing comma
        hist_file.write('\n')
        
hist_file.close()


#-----------------------CALCULATE AND PRINT TIME OF THE SIMULATION-------------
t1 = time.time()

total = t1-t0
print ("The total time is.. ", total)
print ("the time per individual is... ", (float(total)/(float(NPOP*NGEN))))
