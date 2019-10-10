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
    
def esta_cod(file,fstrow):
    return pd.read_csv(file,delimiter=';',decimal=",",header=0,skiprows=fstrow,index_col=False,usecols=[0]).loc[0,'EstacaoCodigo']

def esta_dados(file,fstrow,fstcol):
    return pd.read_csv(file,delimiter=';',decimal=",",header=0,skiprows=fstrow,index_col=False,usecols=fstcol)

def wholedata(path,fstrow,fstcol):
    pwd = ls(path)
    data = pd.DataFrame()
    for i, _ in enumerate(pwd):
        tmp = esta_dados(pwd[i],fstrow,fstcol)
        data = pd.concat([data,tmp])
    data = data.reset_index(drop=True)
    return data

data = wholedata(chuvas,12,range(13))

data["Data"] = pd.to_datetime(data["Data"],yearfirst=True)

tmp = data.iloc[:,0:6]

tmp = tmp.drop(columns=["TipoMedicaoChuvas","NivelConsistencia"])

tmp.dropna(inplace=True)

tmp['EstacaoCodigo'].value_counts()

tmp.groupby('EstacaoCodigo').size()

tempo = tmp.drop('Data', axis=1)

sns.set_palette('husl', 5)
sns.pairplot(tempo, hue='EstacaoCodigo', markers='*')
plt.show()

#x_axis = tmp['Data']
#y_axis = tmp.drop(columns="Data")#
#plt.show()

'''
print(data.dtypes)

data["Maxima"] = pd.to_numeric(data["Maxima"])
data["Total"] = pd.to_numeric(data["Total"])
'''

#chuva stations = sorted([esta_cod(ls(chuvas)[i],12) for i, _ in enumerate(ls(chuvas))])