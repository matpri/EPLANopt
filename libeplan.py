# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:07:53 2015

@author: ufilippi, ggaregnani

EnergyPLAN input utility routines
"""

import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas
import subprocess
from collections import OrderedDict
import os.path
import time
#from libfun import load_json
from constants import HOURS_IN_LEAP_YEAR
import pandas as pd

def is_float_try(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def input2outputRES(inputRES):
    """
    read the json with the rules for the conversion
    from the input file name of RES into the output name
    and return the output name.
    >>> input2outputRES(['Photo Voltaic'])
    [u'PV']
    """
    # in2out = load_json('input2outputRES.json')
    in2out ={
        "Wind": "Wind",
        "Offshore Wind": "Offshore",
        "Photo Voltaic": "PV",
        "Wave Power": "Wave",
        "River Hydro": "River",
        "Tidal": "Tidal",
        "CSP Solar Power": "CSP"}

    outRES = []
    for inp in inputRES:
        for k in in2out.keys():
            if inp == k:
                outRES.append(in2out[k])
    return outRES


class Node(object):
    # of each node I have input values and input ditribution
    def __init__(self, inputfile, eplanfolder,
                 resultsfile=None, data=None, distributions=None,
                 ):

        #TODO: check that the distribution is an object Distribution

        self.inputfile = inputfile
        self.eplanfolder = eplanfolder
        self.resultsfile = resultsfile
        if data is None:
            self.data = self.get_data()
        else:
            self.data = data
        #TODO: data is an order dictionary, to check

        self.distributions = distributions

    def get_data(self):
        #FIXME: fix order dictionary for 3.3
        with open(self.inputfile, 'r') as f:

            # NOTE: make sure input files are ANSI. Input files found in
            # EnergyPLAN folder may be UCS-2 Little Endian.

            data = f.readlines()

            # remove newline character '\n'
            data = [row[:-1] for row in data]
        #import ipdb; ipdb.set_trace()
        od = OrderedDict()
        #print data
        od['Node name'] = self.inputfile  # first key is node name
        for k in np.arange(0, len(data), 2):  # even rows contain keys
            val = data[k + 1]
            # convert val into float/int
            try:
                val = float(val)
                if val.is_integer():
                    val = int(val)
            except:
                pass
            od[data[k].strip('=')] = val

        # remove 'xxx' key, if present
        if 'xxx' in od:
            del od['xxx']

        self.data = od
        return self.data

    def write_input(self):
        """lod --- list of ordered dictionaries with the inputs to write,
        one for each node"""

        od = self.data
        odi = od.items()
        with open(self.inputfile, 'w') as f:
            # 'EnergyPLAN version' is without ending '=', all following inputs
            # are (except for the 'xxx' lines)
            f.write(list(odi)[1][0] + '\n')
            f.write(str(list(odi)[1][1]) + '\n')
            for j in range(2, len(list(odi))):
                f.write(list(odi)[j][0] + '=\n')
                f.write(str(list(odi)[j][1]) + '\n')

                # NOTE: EnergyPLAN seems to ignore present or missing final
                # 'xxx' lines; therefore, we don't add them

    #FIXME: method to excute the node, EPLANFOLDER is it GLOBAL or not
    def excute(self):
        subprocess.call([os.path.join(self.eplanfolder,
                        'energyplan.exe'), '-i',
                         self.inputfile, '-ascii', self.resultsfile])

    def get_distributions(self):
        dfolder = os.path.join(self.eplanfolder,
                               r'energyPlan Data\Distributions')
        # list of the distribution in the eplanfolder
        l_txt = [f for f in self.data.values() if (isinstance(f, str) and
                 f.endswith('txt'))]
        onlyfiles = [f for f in listdir(dfolder) if isfile(join(dfolder, f))]
        l_distr = list(set(l_txt) & set(onlyfiles))
        self.distributions = Distributions(l_distr, self.eplanfolder)
        return self.distributions
        
    def read_annual_indicator(self):
        """read the output file of energyPLAN and return a dictionary
        with the main annual indicators"""
        while not os.path.exists(self.resultsfile):
            time.sleep(1)

        if os.path.isfile(self.resultsfile):
            raw_file = open(self.resultsfile)
            complete = raw_file.read()
            list_file = complete.split("\n")
            y_ind = load_json("out_dict.json")
#            keys = ('SHARE OF RES (incl. Biomass)',
#                    'ANNUAL CO2 EMISSIONS (kt)',
#                    'ANNUAL FUEL CONSUMPTIONS (GWh/year)')
            for k in y_ind.keys():
                if k in 'ANNUAL COSTS (1000 EUR)':
                    for i in y_ind[k].keys():
                        if i in 'TOTAL':
                            ind = 1
                        else:
                            ind = 2
                        for j in y_ind[k][i].keys():
                            val = [s for s in list_file[3:]
                                   if j in s][0].split('\00')[ind]
                            y_ind[k][i][j] = val
                else:
                    for i in y_ind[k].keys():
                        val = [s for s in list_file[3:]
                               if i in s][0].split('\00')[1]
                        y_ind[k][i] = val
            return y_ind
        else:
            raise ValueError("%s isn't a file!" % self.resultsfile)
        
    def read_annual_GWh(self):
        """ read energy demand and production from energyPLAN output file
        """
        while not os.path.exists(self.resultsfile):
            time.sleep(1)

        if os.path.isfile(self.resultsfile):
            raw_file = open(self.resultsfile)
            complete = raw_file.read()
            list_file = complete.split("\n")
            name = list_file[80].split('\x00')[1:]
            field = list_file[81].split('\x00')[1:]
            values = list_file[84].split('\x00')[1:]
            keys = zip(name, field)
            annual_GWh = {}
            for k, v in zip(keys, values):
                k = tuple([i.strip() for i in k])
                try:
                    val = float(v)
                except:
                    val = v
                annual_GWh[k] = val
            return annual_GWh

    def get_annual_GWh(self, inputRES):
        """ given a list with the RES source in the input file, return
        the GWh production
        :param inputRES: list of RES
        :type: list
        """
        annual_GWh = self.read_annual_GWh()
        outRES = input2outputRES(inputRES)
        out_RES_val = []
        for out in outRES:
            for k in annual_GWh.keys():
                if out.strip() == k[0].strip() and k[1].strip() == 'Electr.':
                    # This is done only for the electrical sources
                    out_RES_val.append(annual_GWh[k])
        return out_RES_val
        
   
    def read_indicators(self):
        # unit_CO2=float(list_file[16][38:46])
        # unit_Costs=float(list_file[16][38:46])
        raw_file=open(self.resultsfile)
        complete =raw_file.read()
        list_file= complete.split("\n")
        lista=[]
        for a in range(len(list_file)):
            # row=[]
            list_file2= list_file[a].split("\t")
            lista.append([x.strip() for x in list_file2 if x])
        # print(lista[16:26])
        
        indicators=lista[16:69]
        dic={}
        for a in range(len(indicators)):
            if len(indicators[a])>2:
                if is_float_try(indicators[a][1]):
                    key=indicators[a][0]
                    obj=float(indicators[a][1])
                    if key!='' and obj!='':
                        dic[key]=obj
        return dic
    
    def read_costs_tech(self):
        raw_file=open(self.resultsfile)
        complete =raw_file.read()
        list_file= complete.split("\n")
        lista=[]
        for a in range(len(list_file)):
            # row=[]
            list_file2= list_file[a].split("\t")
            lista.append([x.strip() for x in list_file2 if x])
        # print(lista[16:26])
         
        #costs of the technologies
        dic2={}
        list_var=['Solar thermal', 'Small CHP units', 'Heat Pump gr. 2', 'Heat Storage CHP', 
                  'Large CHP units', 'Heat Pump gr. 3', 'Heat Storage Solar', 'Boilers gr. 2 and 3',
                  'Large Power Plants', 'Wind', 'Wind offshore', 'Photo Voltaic', 'Wave power',
                  'River of hydro', 'Hydro Power', 'Hydro Storage', 'Hydro Pump', 'Nuclear',
                  'Geothermal Electr.', 'Electrolyser', 'Hydrogen Storage', 'Charge el1 storage', 
                  'Discharge el1 storage', 'El1 storage cap', 'Indv. boilers', 'Indv. CHP', 
                  'Indv. Heat Pump', 'Indv. Electric heat','Indv. Solar thermal', 'BioGas Upgrade' ,'Gasification Upgrade',
                  'DHP Boiler group 1', 'Waste CHP', 'Absorp. HP (Waste)', 'Biogas Plant', 
                  'Gasification Plant', 'BioDiesel Plant', 'BioPetrol Plant', 'BioJPPlant', 
                  'Tidal Power', 'CSP Solar Power', 'Carbon Recycling', 'Methanation' ,'Liquidation + JP',
                  'Desalination Plant', 'Water storage', 'Gas Storage', 'Oil Storage' ,'Methanol Storage',
                  'Interconnection', 'Geothermal Heat', 'Indust. Excess Heat', 'Indust. CHP Electr.',
                  'Indust. CHP Heat', 'Electr Boiler Gr 2+3', 'Bicycles' ,'Motorbikes', 'Electric Cars',
                  'Conventional Cars', 'DME Buses', 'Diesel Buses', 'DME Trucks', 'Diesel Trucks', 
                  'El1 storage cap']
        costs_tech=lista[7:73]
        # print( costs_tech)
        list_found=[]
        for a in range(len(costs_tech)):
            for b in range(len(list_var)):
                if list_var[b] in costs_tech[a] and list_var[b] not in list_found:
                    indexList=costs_tech[a].index(list_var[b])
                    key2=costs_tech[a][indexList]
                    dic_temp={}
                    value1=float(costs_tech[a][indexList+1])
                    value2=float(costs_tech[a][indexList+2])
                    value3=float(costs_tech[a][indexList+3])
                    dic_temp['Total Inv. Costs']=value1
                    dic_temp['Annual Inv. Costs']=value2
                    dic_temp['Fixed O&M']=value3
                    dic2[key2]=dic_temp
                    list_found.append(list_var[b])
                elif list_var[b] in costs_tech[a] and list_var[b] in list_found:
                    indexList=costs_tech[a].index(list_var[b])
                    key2=costs_tech[a][indexList]+' doublekey'
                    dic_temp={}
                    value1=float(costs_tech[a][indexList+1])
                    value2=float(costs_tech[a][indexList+2])
                    value3=float(costs_tech[a][indexList+3])
                    dic_temp['Total Inv. Costs']=value1
                    dic_temp['Annual Inv. Costs']=value2
                    dic_temp['Fixed O&M']=value3
                    dic2[key2]=dic_temp
                    list_found.append(key2)
                        
        return dic2
    
    def read_TWh(self):
        raw_file=open(self.resultsfile)
        complete =raw_file.read()
        list_file= complete.split("\n")
        lista=[]
        for a in range(len(list_file)):
            # row=[]
            list_file2= list_file[a].split("\t")
            lista.append([x.strip() for x in list_file2 if x])
        # print(lista[16:26])
         
        #costs of the technologies
        dic3={}
        TWh=lista[80:86]
        # print(TWh)
        list_found=[]
        # list_keys=[]
        # list_values=[]
        for a in range(len(TWh[0])):
            if is_float_try(TWh[4][a]):
                if TWh[1][a]=='':
                    if TWh[0][a]+''+TWh[1][a] not in list_found:
                        dic3[TWh[0][a]+''+TWh[1][a]]=float(TWh[4][a])
                        list_found.append(TWh[0][a]+''+TWh[1][a])
                    else:
                        dic3[TWh[0][a]+''+TWh[1][a]+' doublekey']=float(TWh[4][a])
                        list_found.append(TWh[0][a]+''+TWh[1][a]+' doublekey')
                else:
                    if TWh[0][a]+' '+TWh[1][a] not in list_found:
                        dic3[TWh[0][a]+' '+TWh[1][a]]=float(TWh[4][a])
                        list_found.append(TWh[0][a]+' '+TWh[1][a])
                    else:
                        dic3[TWh[0][a]+' '+TWh[1][a]+' doublekey']=float(TWh[4][a])
                        list_found.append(TWh[0][a]+' '+TWh[1][a]+' doublekey')                    
                # list_keys.append(TWh[0][a]+' '+TWh[1][a])
                # list_values.append(TWh[4][a])
    
        return dic3

    def read_All_outputs(self):
        # unit_CO2=float(list_file[16][38:46])
        # unit_Costs=float(list_file[16][38:46])
        raw_file=open(self.resultsfile)
        complete =raw_file.read()
        list_file= complete.split("\n")
        lista=[]
        for a in range(len(list_file)):
            # row=[]
            list_file2= list_file[a].split("\t")
            lista.append([x.strip() for x in list_file2 if x])
        # print(lista[16:26])
        
        indicators=lista[16:69]
        dic={}
        for a in range(len(indicators)):
            if len(indicators[a])>2:
                if is_float_try(indicators[a][1]):
                    key=indicators[a][0]
                    obj=float(indicators[a][1])
                    if key!='' and obj!='':
                        dic[key]=obj
                        
        TWh=lista[80:86]
        # print(TWh)
        list_found=[]
        # list_keys=[]
        # list_values=[]
        for a in range(len(TWh[0])):
            if is_float_try(TWh[4][a]):
                if TWh[1][a]=='':
                    if TWh[0][a]+''+TWh[1][a] not in list_found:
                        dic[TWh[0][a]+''+TWh[1][a]]=float(TWh[4][a])
                        list_found.append(TWh[0][a]+''+TWh[1][a])
                    else:
                        dic[TWh[0][a]+''+TWh[1][a]+' doublekey']=float(TWh[4][a])
                        list_found.append(TWh[0][a]+''+TWh[1][a]+' doublekey')
                else:
                    if TWh[0][a]+' '+TWh[1][a] not in list_found:
                        dic[TWh[0][a]+' '+TWh[1][a]]=float(TWh[4][a])
                        list_found.append(TWh[0][a]+' '+TWh[1][a])
                    else:
                        dic[TWh[0][a]+' '+TWh[1][a]+' doublekey']=float(TWh[4][a])
                        list_found.append(TWh[0][a]+' '+TWh[1][a]+' doublekey')                    
                # list_keys.append(TWh[0][a]+' '+TWh[1][a])
                # list_values.append(TWh[4][a])
        return dic
    
    def read_hourly_values(self):
        # raw_file = open(FileName)
        raw_file=open(self.resultsfile)
        complete =raw_file.read()
        list_file= complete.split("\n")
        lista=[]
        for a in range(len(list_file)):
            # row=[]
            list_file2= list_file[a].split("\t")
            lista.append([x.strip() for x in list_file2 if x])
        # print(lista[16:26])
         
        #costs of the technologies
        dic3={}
        TWh=lista[80:86]
        TWh_val=lista[105:-1]
        # print(TWh_val[0:5])
        list_found=[]
        # list_keys=[]
        # list_values=[]
        hours=[]
        for a in range(len(TWh[0])):
            # if is_float_try(TWh[4][a]):
            if TWh[1][a]=='':
                if TWh[0][a]+''+TWh[1][a] not in list_found:
                    # dic3[TWh[0][a]+''+TWh[1][a]]=float(TWh[4][a])
                    list_found.append(TWh[0][a]+''+TWh[1][a])
                else:
                    # dic3[TWh[0][a]+''+TWh[1][a]+' doublekey']=float(TWh[4][a])
                    list_found.append(TWh[0][a]+''+TWh[1][a]+' doublekey')
            else:
                if TWh[0][a]+' '+TWh[1][a] not in list_found:
                    # dic3[TWh[0][a]+' '+TWh[1][a]]=float(TWh[4][a])
                    list_found.append(TWh[0][a]+' '+TWh[1][a])
                else:
                    # dic3[TWh[0][a]+' '+TWh[1][a]+' doublekey']=float(TWh[4][a])
                    list_found.append(TWh[0][a]+' '+TWh[1][a]+' doublekey')                    
                # list_keys.append(TWh[0][a]+' '+TWh[1][a])
                # list_values.append(TWh[4][a])
        # print(list_found)
        # for a in range(len(TWh_val)):
        #     for b in range(len(TWh_val[0]):
        #                    TWh_val[a][b]
        df = pd.DataFrame(TWh_val, columns=list_found)
        df = df.astype(float)
        return df

    def read_output_h(self):
        with open(self.resultsfile, 'r') as f:
            hours_in_leap_years = 8784
            output_col_names = ['Electr. Demand', 'Elec.dem Cooling', 'Fixed Exp/Imp',
                    'DH Demand', 'Wind Electr.', 'Wave Electr.', 'PV Electr.', 
                    'River Electr.', 'Tidal Electr.',  'CSP Electr.',
                    'Offshore Electr.', 'Hydro Electr.', 'Hydro pump',
                    'Hydro storage', 'Hydro Wat-Sup', 'Hydro Wat-Loss',
                    'Solar Heat', 'CSHP 1 Heat', 'Waste 1 Heat',
                    'Boiler 1 Heat', 'CSHP 2 Heat', 'Waste 2 Heat',
                    'Geoth 2 Heat', 'Geoth 2 Steam', 'Geoth 2 Storage',
                    'CHP 2 Heat', 'HP 2 Heat', 'Boiler 2 Heat', 'EH 2 Heat',
                    'ELT 2 Heat', 'Storage2 Heat', 'Balance2 Heat',
                    'CSHP 3 Heat', 'Waste 3 Heat', 'Geoth 3 Heat',
                    'Geoth 3 Steam', 'Geoth 3 Storage', 'CHP 3 Heat',
                    'HP 3 Heat', 'Boiler 3 Heat', 'EH 3 Heat', 'ELT 3 Heat',
                    'Storage3 Heat', 'Balance3 Heat', 'Flexible Electr.',
                    'HP Electr.', 'CSHP Electr.', 'CHP Electr.', 'PP Electr.',
                    'PP2 Electr.', 'Nuclear Electr.', 'Geother. Electr.',
                    'Pump Electr.', 'Turbine Electr.', 'Pumped Storage',
                    'ELT 2 Electr.', 'ELT 2 H2 ELT 2', 'ELT 3 Electr.',
                    'ELT 3 H2 ELT 3', 'V2G Demand', 'V2G Charge',
                    'V2G Discha.', 'V2G Storage', 'Trans H2 Electr.',
                    'Trans H2 Storage', 'CO2Hydro Electr.', 'HH-CHP Electr.',
                    'HH-HP Electr.', 'HH-HP/EB Electr.', 'HH-EB Electr.',
                    'HH-H2 Electr.', 'HH-H2 Storage', 'HH-H2 Prices',
                    'HH Dem. Heat', 'HH CHP+HP Heat', 'HH Boil. Heat',
                    'HH Solar Heat', 'HH Store Heat', 'HH Balan Heat',
                    'Stabil. Load', 'Import Electr.', 'Export Electr.',
                    'CEEP Electr.', 'EEEP Electr.', 'Elmarket Prices',
                    'Elmarket Prod', 'System Prices', 'DKmarket Prices',
                    'Btl-neck Prices', 'Import Payment', 'Export Payment',
                    'Blt-neckPayment', 'Add-exp Payment', 'Boilers', 'CHP2+3',
                    'PP CAES', 'Indi- vidual', 'Transp.', 'Indust. Various',
                    'Demand Sum', 'Biogas', 'Syngas', 'CO2HyGas', 'SynHyGas',
                    'SynFuel', 'Storage', 'Storage Content', 'Sum',
                    'Import Gas', 'Export Gas']
                        
            rows = f.readlines()[105:]
            for k in range(hours_in_leap_years):
                rows[k] = rows[k].split('\x00')[1:-1]
                rows[k] = [float(col) for col in rows[k]]
                dr = pandas.date_range(start='20120101 0:00', end='20121231 23:00',
                               freq='H')
            values_distr = pandas.DataFrame(data=rows, index=dr, columns=output_col_names)
        return values_distr


class Distributions(object):
    """
    :param dnames: list of distribution name
    :type: list
    :param eplanfolder: string with the path of EnergyPlan
    :type: str
    """

    def __init__(self, dnames, eplanfolder, data=None):
        self.dnames = dnames
        self.eplanfolder = eplanfolder
        self.data = self.get_distr()

    def get_distr(self, year=2012):

        dfolder = os.path.join(self.eplanfolder,
                               r'energyPlan Data\Distributions')
        #import ipdb; ipdb.set_trace()
        c = lambda x: float(x.replace(',', '.'))

        distr = np.zeros((HOURS_IN_LEAP_YEAR, len(self.dnames)))

        for k in range(len(self.dnames)):
            # I notice in the file Hour.eletricity / as comment
            distr[:, k] = np.genfromtxt(os.path.join(dfolder,
                                        self.dnames[k]),
                                        converters={0: c},
                                        comments='/')

        dr = pandas.date_range(start=str(year)+'0101 0:00',
                               end=str(year)+'1231 23:00',
                               freq='H')
        self.data = pandas.DataFrame(data=distr, index=dr, columns=self.dnames)
        return self.data

    def write_distr(self):

        # convert series to dataframe
        if isinstance(self.data, pandas.Series):
            self.data = pandas.DataFrame(self.data)

        dfolder = os.path.join(self.eplanfolder,
                               r'energyPlan Data\Distributions')

        for s in self.data:
            self.data[s].to_csv(os.path.join(dfolder, s),
                                index=False, sep=';', decimal=',',
                                float_format='%.9f')

    #TODO: can be usefull to have a method that changes values of a
    # a distribution, maybe not because we have methods of dataframe
    def change_distr(self):
        pass









