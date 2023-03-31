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
#df_hist = pd.read_csv('history_csv100.csv', encoding = "ISO-8859-1")
df_hist = pd.read_excel('output.xlsx', encoding = "ISO-8859-1")
df_hist = df_hist.loc[:, ~df_hist.columns.str.contains('^Unnamed')][1:]
df_hist = df_hist.convert_objects(convert_numeric=True)
#df_hist = pd.to_numeric(df_hist)#convert_objects(convert_numeric=True)
#print(df_hist)
dic=df_hist.T.to_dict('list')
#print(dic)
list_individuals=[]
for a in range(len(dic)):
#    print(dic[a+1][-1])
    row=[dic[a+1][-2], dic[a+1][-1]]
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
    df_pareto= df_pareto.append(df_el)

'''create a result xlsx file with hist and pareto'''
#     Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pareto.xlsx', engine='xlsxwriter')

df_hist.to_excel(writer, sheet_name='history')
df_pareto.to_excel(writer, sheet_name='Pareto')
    
#     Close the Pandas Excel writer and output the Excel file.
writer.save()

#'''plot the results'''
#CO2_ind=51.16 #[Mt]
#cost_ind=4714 #[M€]
##cost_ind=35851 #[M€]
##cost_ind=7951.73 #[M€]
#
#df_hist['CO2']=df_hist.loc[:,'CO2 [Mt]']+CO2_ind
#df_hist['Costs']=df_hist.loc[:,'Costs [M€]']+cost_ind
#df_pareto['CO2']=df_pareto.loc[:,'CO2 [Mt]']+CO2_ind
#df_pareto['Costs']=df_pareto.loc[:,'Costs [M€]']+cost_ind
#
#xhist= df_hist['CO2']
#yhist= df_hist['Costs']
#xpar= df_pareto['CO2']
#ypar= df_pareto['Costs']
#
#fig, ax = plt.subplots(figsize=(14,8))
#
#ax.scatter(xhist, yhist, marker='o', c='blue')
#ax.scatter(xpar, ypar, marker='o', c= 'green')
#ax.scatter(278.58+CO2_ind, 69524.27+cost_ind, marker='o', s=100, c= 'red')
##ax.scatter(331.77, 62649.82+cost_ind, marker='o', s=90, c= 'orange')
#
#ax.set_xlabel('CO2 emissions [Mt]')
#ax.set_ylabel('Total annual costs [M€]')
##plt.legend()
#plt.grid()
#plt.show()
#
#pylab.savefig("Pareto.png", bbox_inches="tight", dpi=300)