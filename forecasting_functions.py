# -*- coding: utf-8 -*-
"""forecasting_functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jgYuLpvE4fzF52pFufyLB3ub6LTrmbkE
"""

import numpy as np 
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
from warnings import catch_warnings
from warnings import filterwarnings
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def simple_forecast(history, config):
  n, offset, avg_type = config
  # persist value, ignore other config
  if avg_type == 'persist':
    return history[-n]
  # collect values to average
  values = list()
  if offset == 1:
    values = history[-n:]
  else:
    # skip bad configs
    if n*offset > len(history):
      raise Exception('Config beyond end of data: %d %d' % (n,offset))
    # try and collect n values using offset
    for i in range(1, n+1):
      ix = i * offset
      values.append(history[-ix])
  # check if we can average
  if len(values) < 2:
    raise Exception('Cannot calculate average')
  # mean of last n values
  if avg_type == 'mean':
    return np.mean(values)
  # median of last n values
  return np.median(values)

# one-step Holt Winters Exponential Smoothing forecast
def exp_smoothing_forecast(history, config):
  t,d,s,p,b,r = config
  # define model
  history = np.array(history)
  model = ExponentialSmoothing(history, trend=t, damped=d, seasonal=s, seasonal_periods=p)
  # fit model
  model_fit = model.fit(optimized=True, use_boxcox=b, remove_bias=r)
  # make one step forecast
  yhat = model_fit.predict(len(history), len(history))
  return yhat[0]

# one-step sarima forecast
def sarima_forecast(history, config):
  order, sorder, trend = config
  # define model
  model = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend,
  enforce_stationarity=False, enforce_invertibility=False)
  # fit model
  model_fit = model.fit(disp=False)
  # make one step forecast
  yhat = model_fit.predict(len(history), len(history))
  return yhat[0]

def train_test_split(data, n_test):
  return data[:-n_test], data[-n_test:]

def measure_rmse(actual, predicted):
  return sqrt(mean_squared_error(actual, predicted))

# walk-forward validation for univariate data
def walk_forward_validation(data, n_test, cfg, forecast):
  predictions = list()
  # split dataset
  train, test = train_test_split(data, n_test)
  # seed history with training dataset
  history = [x for x in train]
  # step over each time step in the test set
  for i in range(len(test)):
    # fit model and make forecast for history
    yhat = forecast(history, cfg)
    # store forecast in list of predictions
    predictions.append(yhat)
    # add actual observation to history for the next loop
    history.append(test[i])
  # estimate prediction error
  error = measure_rmse(test, predictions)
  return error

def score_model(data, n_test, cfg, forecast, debug=False):
  result = None
  # convert config to a key
  key = str(cfg)
  forecasts = list()
  # show all warnings and fail on exception if debugging
  if debug:
    result = walk_forward_validation(data, n_test, cfg, forecast)
  else:
    # one failure during model validation suggests an unstable config
    try:
      # never show warnings when grid searching, too noisy
      with catch_warnings():
        filterwarnings("ignore")
        result = walk_forward_validation(data, n_test, cfg, forecast)
    except:
      error = None
  # check for an interesting result
  if result is not None:
    print(' > Model[%s] %.3f' % (key, result))
  return (key, result)

def grid_search(data, cfg_list, n_test, forecast):
  scores = None
  scores = [score_model(data, n_test, cfg, forecast) for cfg in cfg_list]
  # remove empty results
  scores = [r for r in scores if r[1] != None]
  # sort configs by error, asc
  scores.sort(key=lambda tup: tup[1])
  return scores

# create a set of simple configs to try
def simple_configs(max_length, offsets=[1]):
  configs = list()
  for i in range(1, max_length+1):
    for o in offsets:
      for t in ['persist', 'mean', 'median']:
        cfg = [i, o, t]
        configs.append(cfg)
  return configs

def exp_smoothing_configs(seasonal=[None]):
  models = list()
  # define config lists
  t_params = ['add', 'mul', None]
  d_params = [True, False]
  s_params = ['add', 'mul', None]
  p_params = seasonal
  b_params = [True, False]
  r_params = [True, False]
  # create config instances
  for t in t_params:
    for d in d_params:
      for s in s_params:
        for p in p_params:
          for b in b_params:
            for r in r_params:
              cfg = [t,d,s,p,b,r]
              models.append(cfg)
  return models

# create a set of sarima configs to try
def sarima_configs(seasonal=[0]):
  models = list()
  # define config lists
  p_params = [0, 1, 2]
  d_params = [0, 1]
  q_params = [0, 1, 2]
  t_params = ['n','c','t','ct']
  P_params = [0, 1, 2]
  D_params = [0, 1]
  Q_params = [0, 1, 2]
  m_params = seasonal
  # create config instances
  for p in p_params:
    for d in d_params:
      for q in q_params:
        for t in t_params:
          for P in P_params:
            for D in D_params:
              for Q in Q_params:
                for m in m_params:
                  cfg = [(p,d,q), (P,D,Q,m), t]
                  models.append(cfg)
  return models

def plot_forecast(data, n_test, cfg, forecast):
  predictions = list()
  # split dataset
  train, test = train_test_split(data, n_test)
  # seed history with training dataset
  history = [x for x in train]
  # step over each time step in the test set
  for i in range(len(test)):
    # fit model and make forecast for history
    yhat = forecast(history, cfg)
    # store forecast in list of predictions
    predictions.append(yhat)
    # add actual observation to history for the next loop
    history.append(test[i])
  predictions = pd.DataFrame(predictions, index=data.keys()[len(data)-n_test:])
  plt.plot(data)
  plt.plot(predictions)
  plt.show()
  return predictions

