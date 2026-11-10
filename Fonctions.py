#libraries

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import numpy as np
import statsmodels.tsa.stattools as tsa
from scipy.stats import anderson, stats
from scipy.stats import kstest, t
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

#end of libraries


#Import Data from yahoo finance
def get_data(ticker,start_data, end_data):
    try:
        data = yf.download(ticker,start=start_data, end=end_data)
        return(data)
    except Exception as e:
        return f"Error fetching data : {e}"


#cleanning data
def transoData(df) :
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
        df['Daily_Return'] = df['Close'].pct_change()
        return(0)


def DF_test (df) :
    result = tsa.adfuller(df['Close'], regression='ctt')
    print('ADF Statistic : %f' % result[0])
    print('p-value %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s:%f' % (key, value))
    if result[1] > 0.05:
        print('Fail to reject null hypothesis (H0), the data has a unit root and is non-stationary.')
    elif result[1] <= 0.05:
        print('Reject the null hypothesis (H0), the data does not have a unit root and is stationary')






def AD_test(df) :
    rendements_propres = df['Daily_Return'].dropna()  #delete column of 0
    result = anderson(rendements_propres, dist='norm')
    print('Statistic:%3f' % result.statistic)
    for i in range(len(result.critical_values)):
        sl,cv = result.significance_level[i], result.critical_values[i]
        print('Significance Level:%.3f, Critical Value %3f' % (sl,cv))
        if result.statistic < cv :
            print('Sample looks normal (fail to reject H0')
        else :
            print('Sample does not look normal(reject H0)')








def KS_test (df) :
    rendements_propres = df['Daily_Return'].replace([np.inf, -np.inf], np.nan).dropna()
    params = t.fit(rendements_propres)
    d,p_value = kstest(rendements_propres,'t',args=params)
    print(f"KS Statistic: {d}, P-Value: {p_value}")

    if p_value > 0.05:
        print('Sample frits the t-distribution(fail to reject H0)')
    else:
        print('Sample does not fit the t-distribution(reject H0)')



def StudentTest(df):
    rendements_propres = df['Daily_Return'].replace([np.inf, -np.inf], np.nan).dropna() #put terminate value and delete 0 column
    params = t.fit(rendements_propres)
    dfree,mu,std = params
    print(f"Degrees of freedom:{dfree},Mean:{mu}, Standard Deviation: {std}")
    plt.hist(rendements_propres,bins=20, density=True, alpha=0.6, color='g')
    xmin,xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = t.pdf(x, dfree, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = f"Fit results(t-Distribution) : df = {dfree: .2f}, mu={mu : .2f}, std : { std : .2f}"
    plt.title(title)
    plt.show()


def GenererTrajectoires(df, num_simulations=1000, forecast_days=252):
    rendements_propres = df['Daily_Return'].replace([np.inf, -np.inf], np.nan).dropna()
    params = t.fit(rendements_propres)
    df_t, loc, scale = params[0], params[1], params[2]

    simulated_returns = t.rvs(df_t, loc=loc, scale=scale, size=(forecast_days, num_simulations))
    start_price = df['Close'].iloc[-1]
    price_path = np.zeros_like(simulated_returns)
    price_path[0] = start_price

    for k in range(1, forecast_days):
        price_path[k] = np.maximum(price_path[k - 1] * (1 + simulated_returns[k]), 0)

    return price_path  # Le point clé : la fonction renvoie la matrice





#Simulation with plotly better quality graphics but can't analyze over 1000 simulations
def MCSimulPricing(df):
    rendements_propres = df['Daily_Return'].replace([np.inf, -np.inf], np.nan).dropna()  #put terminate value and delete 0 column
    params = t.fit(rendements_propres)
    df_t, loc, scale = params[0], params[1], params[2]
    forecast_days = 252
    num_simulations = 500
    price_path = GenererTrajectoires(df, num_simulations)

    lower_bound = np.percentile(price_path, 5, axis=1)
    upper_bound = np.percentile(price_path, 95, axis=1)
    print("Prix de départ :", price_path[0, 0])
    print("Prix final du premier scénario :", price_path[-1, 0])

    pio.renderers.default = "browser"
    fig = go.Figure()
    for i in range(num_simulations):
        fig.add_trace(go.Scatter(y=price_path[: i], mode='lines', line=dict(color='green', width=1), showlegend=False))

    fig.add_trace(go.Scatter(y=lower_bound, mode='lines', name='5th Percentile',
                             line=dict(color='grey', width=2, dash='dash')))
    fig.add_trace(go.Scatter(y=upper_bound, mode='lines', name='95th Percentile',
                             line=dict(color='blue', width=2, dash='dash')))

    fig.update_layout(title='Monte Carlo simulation of Stock Price with 90% Confidence Interval',
                      xaxis_title='Days',
                      yaxis_title='Stock Close Price $', width=1000, height=600)

    fig.show()



#Simulation with matplotlib can analyze over 1000 simulations but lower quality graphics
def MCSimulPricingPLT(df):
    rendements_propres = df['Daily_Return'].replace([np.inf, -np.inf], np.nan).dropna()
    params = t.fit(rendements_propres)
    df_t, loc, scale = params[0], params[1], params[2]
    num_simulations = 500
    forecast_days = 252

    price_path = GenererTrajectoires(df, num_simulations)

    lower_bound = np.percentile(price_path, 5, axis=1)
    upper_bound = np.percentile(price_path, 95, axis=1)
    print("Prix de départ :", price_path[0, 0])
    print("Prix final du premier scénario :", price_path[-1, 0])

    plt.figure(figsize=(12, 6))
    plt.plot(price_path, linewidth=1, alpha=0.05, color='blue')
    plt.plot(upper_bound, color='red', linewidth=2, label='Borne Supérieure (95%)')
    plt.plot(lower_bound, color='green', linewidth=2, label='Borne Inférieure (5%)')
    plt.title(f"Simulation de Monte Carlo ({num_simulations} scénarios avec intervalle 90%)")
    plt.xlabel("Jours simulés")
    plt.ylabel("Prix de l'action ($)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()



#Pricing Asian Call

def AsianCall (df,strike_price,risk_free_rate = 0.03, num_simulations = 100) :

#1. Extraction des paramètres de la distribution de Student existante

    rendements_propres = df['Daily_Return'].replace([np.inf,-np.inf], np.nan).dropna()
    params = t.fit(rendements_propres)
    df_t,loc,scale = params[0], params[1], params[2]

    forecast_days = 252 # 1 years Maturity

    #Genration of the price trajectory
    price_path = GenererTrajectoires(df, num_simulations)

       #Calculation of the mean value of all possibilities
    average_prices = np.mean(price_path, axis=0)

        #PayOff of an Asian Call

    payoff = np.maximum(average_prices - strike_price, 0)

    T = forecast_days/252.0
    discount_factor = np.exp(-risk_free_rate*T)
    asian_call_price = np.mean(payoff)*discount_factor

    print(f"Pricing Estimation of the Asian Call: (Strike = {strike_price}, r = {risk_free_rate*100}%) : {asian_call_price:.4f} $")

    return asian_call_price


def EuropeanCallPricing(df,strike_price, risk_free_rate = 0.03,num_simulations = 500) :
    #Extration of parameters

    rendements_propres = df['Daily_Return'].replace([np.inf, -np.inf], np.nan).dropna()
    params = t.fit(rendements_propres)
    df_t, loc, scale = params[0], params[1], params[2]

    forecast_days = 252
    num_simulations = 500

    #Trajectory generation
    price_path = GenererTrajectoires(df ,num_simulations)
    final_prices = price_path[-1, :]

    #PayOffs EUROPEAN CALL

    payoffs = np.maximum(final_prices-strike_price, 0)

    T = forecast_days/252.0
    discount_factor = np.exp(-risk_free_rate*T)
    euro_call_price = np.mean(payoffs) * discount_factor

    print(f"Pricing Estimation of the EUROPEAN Call: (Strike = {strike_price}, r = {risk_free_rate*100}%) : {euro_call_price:.4f} $")
    return euro_call_price


#Amrican Call soon