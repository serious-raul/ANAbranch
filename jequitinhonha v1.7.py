# -*- coding: utf-8 -*-
"""
Created on Fri Out 03 13:10:04 2019

@author: Raul Dias Barboza
"""
import os
import pandas as pd
import seaborn as sns
#import matplotlib.pyplot as plt

# your current os username:
user = 'unifesp'
downloads = '/home/' + user + '/Downloads/Dados_Raw'

interest =    ['Chuva01', 'Chuva02', 'Chuva03', 'Chuva04', 'Chuva05', 'Chuva06',
               'Chuva07', 'Chuva08', 'Chuva09', 'Chuva10', 'Chuva11', 'Chuva12',
               'Chuva13', 'Chuva14', 'Chuva15', 'Chuva16', 'Chuva17', 'Chuva18',
               'Chuva19', 'Chuva20', 'Chuva21', 'Chuva22', 'Chuva23', 'Chuva24',
               'Chuva25', 'Chuva26', 'Chuva27', 'Chuva28', 'Chuva29', 'Chuva30',
               'Chuva31']

'''
#Uncomment for Linux
chuvas =            '/home/' + user + '/Downloads/Dados_Raw/chuvas'
cotas =             '/home/' + user + '/Downloads/Dados_Raw/cotas'
#curvadescarga =     '/home/' + user + '/Downloads/Dados_Raw/curvadescarga'
#PerfilTransversal = '/home/' + user + '/Downloads/Dados_Raw/PerfilTransversal'
#qualagua =          '/home/' + user + '/Downloads/Dados_Raw/qualagua'
#ResumoDescarga =    '/home/' + user + '/Downloads/Dados_Raw/ResumoDescarga'
#sedimentos =        '/home/' + user + '/Downloads/Dados_Raw/sedimentos'
vazoes =            '/home/' + user + '/Downloads/Dados_Raw/vazoes'
'''

#Uncomment for Windows
chuvas =            'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\chuvas'
cotas =             'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\cotas'
curvadescarga =     'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\curvadescarga'
PerfilTransversal = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\PerfilTransversal'
qualagua =          'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\qualagua'
ResumoDescarga =    'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\ResumoDescarga'
sedimentos =        'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\sedimentos'
vazoes =            'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\vazoes'


irape_date = '01-06-2006'

def ls(path):
    ''' r=root, d=directories, f = files '''
    return [os.path.join(r, file)
            for r, _, f in os.walk(path)
            for file in f
            if '.csv' in file]

def stationCode(file,skiprows=12):
    return pd.read_csv(file, delimiter=';',
                       decimal=",",
                       header=0,
                       skiprows=skiprows,
                       index_col=False,
                       usecols=[0]).loc[0, 'EstacaoCodigo']

def stationsAt(path):
    return [stationCode(ls(path)[i])
            for i, _ in enumerate(ls(path))]

def stationData(file, skiprows=12):
    return pd.read_csv(file, delimiter=';',
                       decimal=",",
                       header=0,
                       skiprows=skiprows,
                       index_col=False)

def systemData(path, skiprows=12):
    data = pd.DataFrame()
    for i, _ in enumerate(ls(path)):
        tmp = stationData(ls(path)[i], skiprows)
        data = pd.concat([data, tmp])
    return data

def stationAttributes(file, skiprows=12):
    return stationData(file, skiprows).columns

def stationMean(file, target, skiprows=12):
    return stationData(file, skiprows)[target].mean()

def systemMean(path, target):
    return systemData(path)[target].mean()

def stationMeanofMeans(path, target):
    return pd.DataFrame([stationMean(ls(path)[i], target)
                         for i, _ in enumerate(ls(path))]).mean()
        
def stationPath(path,code):
    for i, station in enumerate(stationsAt(path)):
        if station == code:
            return ls(path)[i]
        
###############################################################################
            
itapebi = stationPath(chuvas,1539006)
data = stationData(itapebi)
# Limpei os dados perfeitamente
data.drop(data.columns[0],axis=1,inplace=True)
data.drop(data.columns[0],axis=1,inplace=True)
while data.columns[1] != 'Chuva01':
    data.drop(data.columns[1],axis=1,inplace=True)
daily = pd.melt(data,id_vars='Data')
    
###############################################################################

def normalizeVar(data, target):
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
    data = data.sort_values('Data')
    data = data[['Data', target, 'EstacaoCodigo']]
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)
    return data

def stationLineplot(file, target,
                    minimus=False, maximus=False,
                    after=False, before=False, skiprows=12):
    data = stationData(file, skiprows)
    normalizeVar(data,target)
    if minimus: data = data[data[target] > minimus]
    if maximus: data = data[data[target] < maximus]
    if after: data = data[data['Data'] > after]
    if before: data = data[data['Data'] < before]
    
    sns.set(style="darkgrid")
    sns.set(rc={'figure.figsize':(11.7, 8.27)})#tamanho de um A4
    
    graph = sns.lineplot(x="Data", y=target, data=data)
    return graph
    
def systemLineplot(path, target,
                   minimus=False, maximus=False,
                   after=False, before=False, skiprows=12):
    data = systemData(path, skiprows)
    normalizeVar(data,target)
    if minimus: data = data[data[target] > minimus]
    if maximus: data = data[data[target] < maximus]
    if after: data = data[data['Data'] > after]
    if before: data = data[data['Data'] < before]
    
    sns.set(style="darkgrid")
    sns.set(rc={'figure.figsize':(11.7, 8.27)})#tamanho de um A4
    
    graph = sns.lineplot(x="Data", y=target,
                            legend="full",
                            hue="EstacaoCodigo",
                            data=data)
    graph.legend(loc='center left',
                 bbox_to_anchor=(1, 0.5),
                 ncol=1)
    return graph

###############################################################################










