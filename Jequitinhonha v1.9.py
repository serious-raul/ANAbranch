# -*- coding: utf-8 -*-
"""
Created on Sat Out 19 18:10:04 2019

@author: Raul Dias Barboza
"""
import os
import pandas as pd
import seaborn as sns
from pathlib import Path
#import matplotlib.pyplot as plt

#user = 'familia' # O usuário atual do seu computador
user = str(Path.home())
raw = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw'

# Uncomment for Linux
chuvas =            user + '/Downloads/Dados_Raw/chuvas'
cotas =             user + '/Downloads/Dados_Raw/cotas'
curvadescarga =     user + '/Downloads/Dados_Raw/curvadescarga'
PerfilTransversal = user + '/Downloads/Dados_Raw/PerfilTransversal'
qualagua =          user + '/Downloads/Dados_Raw/qualagua'
ResumoDescarga =    user + '/Downloads/Dados_Raw/ResumoDescarga'
sedimentos =        user + '/Downloads/Dados_Raw/sedimentos'
vazoes =            user + '/Downloads/Dados_Raw/vazoes'

'''
# Uncomment for Windows
chuvas =            'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\chuvas'
cotas =             'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\cotas'
curvadescarga =     'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\curvadescarga'
PerfilTransversal = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\PerfilTransversal'
qualagua =          'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\qualagua'
ResumoDescarga =    'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\ResumoDescarga'
sedimentos =        'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\sedimentos'
vazoes =            'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\vazoes'
'''

#Set color, type and size of plots
sns.set(style="darkgrid")
sns.set(rc={'figure.figsize':(11.7, 8.27)})#tamanho de um A4

###############################################################################
# As primeiras funções auxiliam a extrair os dados dos arquivos csv da ANA

def ls(path):
    ''' r=root, d=directories, f = files
    retorna uma lista com os arquivos csv em no caminho passado '''
    return [os.path.join(r, file)
            for r, _, f in os.walk(path)
            for file in f
            if '.csv' in file]

def stationPathtoCode(file,skiprows=12):
    ''' retorna o codigo da estação em um caminho de arquivo '''
    return pd.read_csv(file, delimiter=';',
                       decimal=",",
                       header=0,
                       skiprows=skiprows,
                       index_col=False,
                       usecols=[0]).loc[0, 'EstacaoCodigo']

def stationCodetoPath(path,code):
    ''' retorna o caminho de um arquivo que tem o código da estação '''
    for i, station in enumerate(stationsAt(path)):
        if station == code:
            return ls(path)[i]

def stationsAt(path):
    ''' retorna o codigo de estação de todos os arquivos em um caminho '''
    return [stationPathtoCode(ls(path)[i])
            for i, _ in enumerate(ls(path))]

def stationData(file, skiprows=12):
    ''' retorna um dataframe com os dados de um arquivo '''
    return pd.read_csv(file, delimiter=';',
                       decimal=",",
                       header=0,
                       skiprows=skiprows,
                       index_col=False)

def systemData(path, skiprows=12):
    ''' retorna um dataframe com os dados de vários arquivos em um caminho '''
    data = pd.DataFrame()
    for i, _ in enumerate(ls(path)):
        tmp = stationData(ls(path)[i], skiprows)
        data = pd.concat([data, tmp])
    return data

###############################################################################
# As funções a seguir atuam em dataframes criados com as funções anteriores

def stationAttributes(data):
    ''' retorna o cabeçalho das colunas de um arquivo '''
    return data.columns

def stationMean(data, target):
    ''' retorna a média aritimética de um atributo alvo de um arquivo '''
    return data[target].mean()

def systemMean(path, target):
    ''' retorna a média aritimética de um atributo alvo dos arquivos de um caminho '''
    return systemData(path)[target].mean()

def stationMeanofMeans(path, target):
    ''' retorna a média das média aritimética de um atributo alvo dos arquivos de um caminho '''
    return pd.DataFrame([stationMean(ls(path)[i], target)
                         for i, _ in enumerate(ls(path))]).mean()

# E as funções que serão mais utilizadas:
        
def datetimeSorted(data):
    ''' converte a coluna 'Data' para datetime se não estiver e ordena cronológicamente '''
    if data['Data'].dtypes != 'datetime64':
        data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
    data = data.sort_values('Data')
    data = data.reset_index(drop=True)
    return data

def targetVar(data, target):
    ''' retorna um série apenas com as ocorrências não nulas de um atributo alvo de um dataframe '''
    data = data[['Data', target]]
    data.dropna(inplace=True)
    return data

###############################################################################
# As funções abaixo plotam gráficos de linha utilizando tais dataframes
    
def stationLineplot(data, target,
                    after=False, before=False,
                    minimus=False, maximus=False):
    ''' retorna um gráfico de linha do atributo alvo pelo tempo 
    utilizando os dados do dataframe passado '''
    data = datetimeSorted(data)
    data = targetVar(data,target)
    
    if minimus: data = data[data[target] > minimus]
    if maximus: data = data[data[target] < maximus]
    if after: data = data[data['Data'] > after]
    if before: data = data[data['Data'] < before]
    
    return sns.lineplot(x="Data", y=target, data=data)
    
def systemLineplot(path, target,
                   after=False, before=False,
                   minimus=False, maximus=False, skiprows=12):
    ''' retorna um gráfico de linha do atributo alvo pelo tempo 
    utilizando os dados de todos os arquivos csv do caminho passado '''
    data = systemData(path, skiprows)
    data = datetimeSorted(data)
    targetVar(data,target)
    
    if minimus: data = data[data[target] > minimus]
    if maximus: data = data[data[target] < maximus]
    if after: data = data[data['Data'] > after]
    if before: data = data[data['Data'] < before]
    
    graph = sns.lineplot(x="Data", y=target, legend="full",
                            hue="EstacaoCodigo", data=data)
    
    graph.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    return graph

###############################################################################
# Trabalhando com os dados diários em forma de séries temporais
    
def dailyOccurences(data,target=['Chuva01','Vazao01','Cota01']):
    ''' retorna apenas as ocorrencias diárias do dataframe.
    a primeira coluna é a data as outras 31 são as ocorrências '''
    target = list(set(target).intersection(data.columns))[0]
    while data.columns[0] != 'Data': data.drop(data.columns[0],axis=1,inplace=True)
    while data.columns[1] != target: data.drop(data.columns[1],axis=1,inplace=True)
    while len(data.columns) > 32: data.drop(data.columns[32],axis=1,inplace=True)
    return data

def dailySeries(data):
    ''' retorna uma série temporal de um dataframe que contenha
    apenas ocorrencias diárias '''
    data = pd.melt(data, id_vars='Data')
    data.dropna(inplace=True)
    data = datetimeSorted(data)
    return data

def checkStation(code):
    ''' procura pelo codigo da estação nos diretórios e retorna True caso encontre '''
    print('Checado em: chuvas, vazoes, cotas')
    return code in stationsAt(chuvas), code in stationsAt(vazoes), code in stationsAt(cotas)

###############################################################################
# Utilizando as funções para trabalhar os dados

graomogolvazao = stationCodetoPath(vazoes, 54150000)