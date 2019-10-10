# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 00:50:04 2019

@author: Raul Dias Barboza
"""
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# your current os username:
user = 'unifesp'

'''
#Uncomment for Linux
chuvas = '/home/' + user + '/Downloads/Dados_Raw/chuvas'
cotas = '/home/' + user + '/Downloads/Dados_Raw/cotas'
vazoes = '/home/' + user + '/Downloads/Dados_Raw/vazoes'
'''

#Uncomment for Windows
chuvas = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\chuvas'
cotas = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\cotas'
vazoes = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\vazoes'


def ls(path):
    # r=root, d=directories, f = files
    return [os.path.join(r, file)
            for r, _, f in os.walk(path)
            for file in f
            if '.csv' in file]

def stationCode(file):
    return pd.read_csv(file,delimiter=';',decimal=",",header=0,skiprows=12,index_col=False,usecols=[0]).loc[0,'EstacaoCodigo']

def stations(path):
    ''' retorna uma lista com o código de todas as estacoes
    dos arquivos presentes no caminho passado '''
    return [stationCode(ls(path)[i]) for i, _ in enumerate(ls(path))]

def stationData(file,skiprows):
    ''' retorna um pandas.DataFrame com os dados de um
    unico arquivo csv e ignora as 'skiprow' primeiras linhas '''
    return pd.read_csv(file,delimiter=';',decimal=",",header=0,skiprows=skiprows,index_col=False)

def systemData(path,skiprows):
    ''' retorna um pandas.DataFrame com os dados de todos
    os arquivos csv arquivo e ignora as 'skiprow' primeiras linhas '''
    data = pd.DataFrame()
    for i, _ in enumerate(ls(path)):
        tmp = stationData(ls(path)[i],skiprows)
        data = pd.concat([data,tmp])
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
    data = data.sort_values('Data')
    return data

def stationLineplot(file,target):
    data = stationData(file,12)
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
    data = data.sort_values('Data')
    data = data[['Data',target,'EstacaoCodigo']]
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)
    
    sns.set(style="darkgrid")
    sns.set(rc={'figure.figsize':(11.7, 8.27)})
    sns.lineplot(x="Data", y=target, data=data)
    
def systemLineplot(path,target):
    data = systemData(path,12)
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
    data = data.sort_values('Data')
    data = data[['Data',target,'EstacaoCodigo']]
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)
    
    sns.set(style="darkgrid")
    sns.set(rc={'figure.figsize':(11.7, 8.27)})
    
    graph = sns.lineplot(x="Data", y=target,
                            legend="full",
                            hue="EstacaoCodigo",
                            data=data)
    
    graph.legend(loc='center left',
                 bbox_to_anchor=(1, 0.5),
                 ncol=1)
'''    
def chooseLineplot(path,target):
    data = systemData(path,12)
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
    data = data.sort_values('Data')
    data = data[['Data',target,'EstacaoCodigo']]
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)
    data = data[data["Media"] < 1000]
    
    sns.set(style="darkgrid")
    sns.set(rc={'figure.figsize':(11.7, 8.27)})
    
    graph = sns.lineplot(x="Data", y=target,
                            legend="full",
                            hue="EstacaoCodigo",
                            data=data)
    
    graph.legend(loc='center left',
                 bbox_to_anchor=(1, 0.5),
                 ncol=1)
''' 
    












