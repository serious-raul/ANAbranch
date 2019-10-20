# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 18:24:16 2019

ANAbranch(jequitinhonha v2.0)
"""
###############################################################################

import anabranch as ab # funções para trabalhar com os arquivos da ANA
import keystations as ks # estações do jequitinhonha importantes para o estudo
''' Bibliotecas necessárias para o ARIMA '''
import warnings
import itertools
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Cor, tipo e forma dos Gráficos
plt.style.use('fivethirtyeight')
sns.set(style="darkgrid")
sns.set(rc={'figure.figsize':(11.7, 8.27)})
sns.set_context("paper", rc={"lines.linewidth": 2})

###############################################################################

sample = ks.graomogolvazao # usando os dados dessa estação

data = ab.stationData(sample) # na forma de dataframe
data = ab.dailyOccurences(data) # apenas as ocorrencias diárias
data = ab.dailySeries(data) # no formato de série temporal
data = ab.datetimeSorted(data) # em ordem cronológica
data = ab.targetVar(data,'value') # apenas a variável alvo
#data = data[data['Data'] > '1975'] # entre 1975
data = data[data['Data'] < '2006'] # e 2006
data = data.set_index('Data') # usando as Datas como índice

###############################################################################

y = data # como os dados estão no formato correto podemos definilo como 'y'
y = y['value'].resample('MS').mean()
y.dropna(inplace=True)

y.plot(figsize=(11.7, 8.27))

plt.show(sns)

sns.lineplot(x=data.index, y=data['value'], data=data)
sns.lineplot(x=data.index, y=data['value'].mean(), data=data)

###############################################################################

from pylab import rcParams
rcParams['figure.figsize'] = 11.7, 8.27

y.isnull().sum()

decomposition = sm.tsa.seasonal_decompose(y, model='additive', freq=12)
fig = decomposition.plot()
plt.show(sns)

###############################################################################

# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

###############################################################################

#\BEGIN{FORUM CODE}
warnings.filterwarnings("ignore") # specify to ignore warning messages
AIC_list = pd.DataFrame({}, columns=['param','param_seasonal','AIC'])
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()

            print('ARIMA{}x{} - AIC:{}'.format(param, param_seasonal, results.aic))
            temp = pd.DataFrame([[ param ,  param_seasonal , results.aic ]], columns=['param','param_seasonal','AIC'])
            AIC_list = AIC_list.append( temp, ignore_index=True)  # DataFrame append 는 일반 list append 와 다르게 이렇게 지정해주어야한다.
            del temp

        except:
            continue

#BIG DIFERENCE, THIS CODE IS A GEM
m = np.amin(AIC_list['AIC'].values) # Find minimum value in AIC
l = AIC_list['AIC'].tolist().index(m) # Find index number for lowest AIC
Min_AIC_list = AIC_list.iloc[l,:]

mod = sm.tsa.statespace.SARIMAX(y,
                                order=Min_AIC_list['param'],
                                seasonal_order=Min_AIC_list['param_seasonal'],
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()

print("### Min_AIC_list ### \n{}".format(Min_AIC_list))

print(results.summary().tables[1])

results.plot_diagnostics(figsize=(11.7, 8.27))
plt.show(sns)
#\END{FORUM CODE}

###############################################################################

pred = results.get_prediction(start=pd.to_datetime('1998-01-01').tz_localize('UTC'), dynamic=False)
pred_ci = pred.conf_int()

ax = y['1990':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Data')
ax.set_ylabel('Vazão')
plt.legend()

plt.show(sns)

###############################################################################

y_forecasted = pred.predicted_mean
y_truth = y['1998-01-01':]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

pred_dynamic = results.get_prediction(start=pd.to_datetime('1998-01-01').tz_localize('UTC'), dynamic=True, full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()

ax = y['1990':].plot(label='observed', figsize=(11.7, 8.27))
pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

ax.fill_between(pred_dynamic_ci.index,
                pred_dynamic_ci.iloc[:, 0],
                pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('1998-01-01').tz_localize('UTC'), y.index[-1],
                 alpha=.1, zorder=-1)

ax.set_xlabel('Date')
ax.set_ylabel('Vazão')

plt.legend()
plt.show(sns)

###############################################################################
'''
# Extract the predicted and true values of our time series
y_forecasted = pred_dynamic.predicted_mean
y_truth = y['1998-01-01':]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

# Get forecast 500 steps ahead in future
pred_uc = results.get_forecast(steps=500)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()

ax = y.plot(label='observed', figsize=(11.7, 8.27))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Data')
ax.set_ylabel('Vazão')

plt.legend()
plt.show(sns)
'''
###############################################################################