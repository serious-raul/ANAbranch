# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 21:22:04 2019

@author: AlunosBS
"""

import os
import pandas as pd

user = 'AlunosBS.LABENGCM07'
#downloads = "c:\\Users\\raul.dias\\Downloads"
chuvas = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\chuvas'
cotas = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\cotas'
vazoes = 'c:\\Users\\' + user + '\\Downloads\\Dados_Raw\\vazoes'

def ls(path):
    # r=root, d=directories, f = files
    return [os.path.join(r, file)
            for r, _, f in os.walk(path)
            for file in f
            if '.csv' in file]
    
def esta_cod(file):
    return pd.read_csv(file,delimiter=';',header=0,skiprows=12,index_col=False,usecols=[0]).loc[0,'EstacaoCodigo']

def esta_dados(file):
    return pd.read_csv(file,delimiter=';',header=0,skiprows=12,index_col=False,usecols=list(range(7)))

df0 = esta_dados(ls(chuvas)[0])
df1 = esta_dados(ls(chuvas)[1])
df2 = esta_dados(ls(chuvas)[2])
df3 = esta_dados(ls(chuvas)[3])
df4 = esta_dados(ls(chuvas)[4])
df5 = esta_dados(ls(chuvas)[5])
df6 = esta_dados(ls(chuvas)[6])
df7 = esta_dados(ls(chuvas)[7])
df8 = esta_dados(ls(chuvas)[8])
df9 = esta_dados(ls(chuvas)[9])
df10 = esta_dados(ls(chuvas)[10])
df11 = esta_dados(ls(chuvas)[11])
df12 = esta_dados(ls(chuvas)[12])

chuvarada = pd.concat([df0,df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12])