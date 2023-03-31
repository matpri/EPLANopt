# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:49:55 2020

@author: MPrina
"""

from GA import GA
from libeplan import Node
from termcolor import colored
import time

global VARIABLES, START, X, MOLT_FACTORS, INPUTFILE
global ENERGYPLAN, OUT_FOLDER, FUNCTION_2_EVAL
global CONSTRAIN

#------------------------------------INPUT DATA--------------------------------
data = {"EnergyPLAN folder": r"C:\Users\MPrina\Desktop\ZIPEnergyPLAN121",
        "Input file": r"C:\Users\MPrina\Desktop\SDEWES 2020\EPLANopt Island\EPLANopt\input_folder\Favignana_baseline_SECAP_ANSI.txt",
        "Output folder": r"C:\Users\MPrina\Desktop\SDEWES 2020\EPLANopt Island\EPLANopt\input_folder",
        "Number of process": 1,
        "Genetic algorithm": {"Size of population": 4,
                               "Number of generations": 1},

        "Variables": [{"EnergyPLAN Name": "input_RES1_capacity", "Range": [17, 100],"Moltiplication factor": 10}, #[10, 50]
                      {"EnergyPLAN Name": 'input_cap_pp_el', "Range": [0, 0],"Moltiplication factor": 10}, #[0, 1]
                      {"EnergyPLAN Name": 'input_storage_pump_cap', "Range": [0, 0],"Moltiplication factor": 10}] #[0, 75]
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
    out_file = r'%s\out_new.txt' % (OUT_FOLDER)

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
        print(new_node)
        dic = new_node.read_output_y()
#        outp = new_node.read_output_DB()
#        print(outp[79:80])
#        print(outp[80:81])
        c.append(1)
        print('a simulation executed, n = %d' %len(c))
        collection[name_ind] = dic #new_node
    
#------------------------------------------------------------------------------
    
    Costs = dic['TOTAL ANNUAL COSTS'] # [M€] 

    CO2 = dic['CO2-emission (total)'] # CO2 [kt]
    print('Costs:', colored(Costs, 'red'), '[M€]')
    print('CO2:', colored(CO2, 'green'), '[kt]')
    return CO2, Costs
    

x=[20, 0, 0]
y=f(x)
print(y)

print ('...............................................')

