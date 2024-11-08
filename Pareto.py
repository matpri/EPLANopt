# -*- coding: utf-8 -*-
"""
Created on Thu May 18 15:51:25 2017

@author: MPrina
"""
import pandas as pd
import pylab
import matplotlib.pyplot as plt
#import xlsxwriter
#import seaborn as sns

def drop_duplicates(lst):
    """List with duplicates removed."""
    return [x for x in {tuple(row) for row in lst}]

def pareto_front(lst):
    """Pareto front from a list of objective function values."""    
    lst = drop_duplicates(lst)
    nlst = len(lst)
    nobj = len(lst[0])
    rng = range(nobj)
    idi = [] # indices of dominated individuals
    for i, row in enumerate(lst):
        for j, row2 in enumerate(lst):
            if i != j:
                if sum([row[x] >= row2[x] for x in rng]) == nobj:
                    # individual i is dominated by individual j
                    idi.append(i)
                    break
    return [lst[x] for x in range(nlst) if x not in idi]

'''read the history_csv.csv file and calculate the pareto front of non-dominated solutions'''
df_hist = pd.read_csv('history_csv.csv', encoding = "ISO-8859-1")
# df_hist = pd.read_excel('output.xlsx')
#df_hist = df_hist.loc[:, ~df_hist.columns.str.contains('^Unnamed')][1:]
# Remove columns with 'Unnamed' in their column names
df_hist = df_hist.loc[:, ~df_hist.columns.str.contains('^Unnamed')]

df_hist = df_hist.apply(pd.to_numeric, errors='coerce')
#df_hist = df_hist.convert_objects(convert_numeric=True)
#df_hist = pd.to_numeric(df_hist)#convert_objects(convert_numeric=True)
#print(df_hist)
print(df_hist)
dic=df_hist.T.to_dict('list')
#print(dic)
list_individuals=[]
for a in range(len(dic)):
#    print(dic[a+1][-1])
    row=[dic[a][-2], dic[a][-1]]
    list_individuals.append(row)
#    print(dic[a][-1])
#print(list_individuals)
pareto = pareto_front(list_individuals)
print(pareto)
#df_pareto=df_hist.loc[df_hist['CO2 emissions [kt]'].isin([x[0] for x in pareto]) & df_hist['Total annual costs [keuro]'].isin([x[1] for x in pareto])]

#print(df_pareto)
df_pareto=pd.DataFrame()
for a in range(len(pareto)):
    df_el= df_hist.loc[(df_hist['CO2 emissions [kt]']== pareto[a][0]) & (df_hist['Total annual costs [keuro]']== pareto[a][1])]
    df_pareto = pd.concat([df_pareto, df_el])
    # df_pareto= df_pareto.append(df_el)

'''create a result xlsx file with hist and pareto'''
#     Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pareto.xlsx', engine='xlsxwriter')

df_hist.to_excel(writer, sheet_name='history')
df_pareto.to_excel(writer, sheet_name='Pareto')
    
#     Close the Pandas Excel writer and output the Excel file.
writer.close()
