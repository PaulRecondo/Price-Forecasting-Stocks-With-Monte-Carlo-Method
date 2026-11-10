import pandas as pd
import Fonctions as f
import yfinance as yf
import numpy as np
import statsmodels.tsa.stattools as tsa
from scipy.stats import anderson, stats
from scipy.stats import kstest, t
import matplotlib as plt
import plotly.graph_objects as go
import plotly.io as pio

ticker_symbol = "PREIX" #T.Rowe price equity index 500 fund
start_date = "2005-01-01"
end_date = "2026-01-01"
stock_data = f.get_data(ticker_symbol,start_date,end_date)
#stock_data.asfreq('B').index

#Augmentetd Dickey-Fuller test for stationarity
f.DF_test(stock_data)


#transfo Data
f.transoData(stock_data)

#Anderson-Darling test for Normal Law
f.AD_test(stock_data)

#Kolmogorov-Smirov test for student distribution
f.KS_test(stock_data)
#T-test (Student Law)
f.StudentTest(stock_data)
#####Price forecast Simulated by Monte Carlo####
#f.MCSimulPricing(stock_data)
f.MCSimulPricingPLT(stock_data)

#Pricing ASIAN CALL
f.AsianCall(stock_data,250,0.02,300)


#Pricing EUROPEAN CALL
f.EuropeanCallPricing(stock_data,150,0.05,300)