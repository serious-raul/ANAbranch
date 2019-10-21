# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 18:24:16 2019

ANAbranch(jequitinhonha v2.0)
"""
###############################################################################

import os
import anabranch as ab
from pathlib import Path

current = os.getcwd()
user = str(Path.home())
raw = user + '/Downloads/Dados_Raw/'

###############################################################################

# Uncomment for Linux
chuvas =            user + '/Downloads/Dados_Raw/chuvas'
cotas =             user + '/Downloads/Dados_Raw/cotas'
curvadescarga =     user + '/Downloads/Dados_Raw/cruvadescarga'
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
###############################################################################
# Utilizando a biblioteca ab para encontrar os dados das estações de interesse

irape_date = '01-06-2006' #2002
itapebi_date = '01-02-2003' #1999

# UTILIZANDO DADOS DA ESTAÇÃO IRAPE
irapevazao = ab.stationCodetoPath(vazoes, 54140000) # irapé é a estação nº 54140000

# imediatamente depois da irape
graomogolchuva = ab.stationCodetoPath(chuvas, 1642007) 
graomogolcota = ab.stationCodetoPath(cotas, 54150000)
graomogolvazao = ab.stationCodetoPath(vazoes, 54150000)

# UTILIZANDO DADOS DA ESTAÇÃO ITAPEBI
itapebichuva = ab.stationCodetoPath(chuvas, 1539006) # itapebi é a estação nº 1539006, essa fica na cidade
itapebivazao = ab.stationCodetoPath(vazoes, 54940000) # essa fica na hirelétrica

# imediatamente depois da itapebi
belmontecota = ab.stationCodetoPath(cotas, 54950000)
belmontevazao = ab.stationCodetoPath(vazoes, 54950000)

# UTILIZANDO DADOS DA ESTAÇÃO BELMONTE
belmontechuva = ab.stationCodetoPath(chuvas, 1538001)

###############################################################################
