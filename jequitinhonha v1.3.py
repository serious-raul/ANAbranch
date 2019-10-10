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
user = 'familia'

#Uncomment for Linux
chuvas = '/home/' + user + '/Downloads/Dados_Raw/chuvas'
cotas = '/home/' + user + '/Downloads/Dados_Raw/cotas'
vazoes = '/home/' + user + '/Downloads/Dados_Raw/vazoes'

'''
#Uncomment for Windows
chuvas = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\chuvas'
cotas = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\cotas'
vazoes = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\vazoes'
'''

def ls(path):
    # r=root, d=directories, f = files
    return [os.path.join(r, file)
            for r, _, f in os.walk(path)
            for file in f
            if '.csv' in file]

def esta_dados(file,fstrow):
    return pd.read_csv(file,delimiter=';',decimal=",",header=0,skiprows=fstrow,index_col=False)

def wholedata(path,fstrow):
    pwd = ls(path)
    data = pd.DataFrame()
    for i, _ in enumerate(pwd):
        tmp = esta_dados(pwd[i],fstrow)
        data = pd.concat([data,tmp])
    return data

def esta_plot(file):
    data = esta_dados(file,12)
    
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
    data = data.sort_values('Data')
    data = data[['Data','Total','EstacaoCodigo']]
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)
    
    sns.set(style="darkgrid")
    
    sns.set(rc={'figure.figsize':(11.7, 8.27)})
    
    graph = sns.lineplot(x="Data", y="Total",
                            legend="full",
                            #hue="EstacaoCodigo",
                            data=data)
    
    graph.legend(loc='center left',
                 bbox_to_anchor=(1, 0.5),
                 ncol=1)


data = wholedata(chuvas,12)

data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', utc=True)
data = data.sort_values('Data')
data = data[['Data','Total','EstacaoCodigo']]
data.dropna(inplace=True)
data = data.reset_index(drop=True)

'''
#All raining records between 2000 and 2017

data = data.pivot_table(index='Data',columns='EstacaoCodigo',values='Total')
data.dropna(inplace=True)
data.plot()
'''


#Good lineplot from every data (some nan)
sns.set(style="darkgrid")

sns.set(rc={'figure.figsize':(117, 82.7)})

graph = sns.lineplot(x="Data", y="Total",
                        legend="full",
                        hue="EstacaoCodigo",
                        data=data)

graph.legend(loc='center left',
             bbox_to_anchor=(1, 0.5),
             ncol=1)


'''
for i, _ in enumerate(ls(chuvas)):
    esta_plot(ls(chuvas)[i])
'''





























