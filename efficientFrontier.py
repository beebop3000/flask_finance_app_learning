import pandas as pd
import numpy as np
import glob
import os

import plotly.graph_objects as go



def load_ef_files():
    # 1. Load all CSVs into one DataFrame
    all_files = glob.glob("data/*.csv")
    prices = pd.DataFrame()

    for file in all_files:
        ticker = os.path.basename(file).replace(".csv", "")
        df = pd.read_csv(file, index_col='Date', parse_dates=True)

        prices[ticker] = df['Close']

    # 2. Calculate Daily Log Returns
    # Log returns are better for additive time series analysis
    returns = np.log(prices / prices.shift(1)).dropna()

    return returns

def ef_simulation(returns):

    # Annualize the data (252 trading days)
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252

    # Settings for simulation
    num_portfolios = 15000
    results = np.zeros((3, num_portfolios)) # Rows: Return, Volatility, Sharpe
    weights_record = []

    for i in range(num_portfolios):
        # 1. Generate random weights that sum to 1.0 (100%)
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        # 2. Calculate Portfolio Return
        portfolio_return = np.sum(weights * mean_returns)
        
        # 3. Calculate Portfolio Risk (Standard Deviation)
        # Formula: sqrt(Weights_Transposed * Covariance_Matrix * Weights)
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # 4. Store [Return, Risk, Sharpe Ratio]
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = portfolio_return / portfolio_std_dev # Sharpe Ratio

    return results


def plot_ef(results):

    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[1,max_sharpe_idx], results[0,max_sharpe_idx]


    fig = go.Figure()

    # 1. The "Cloud" of all simulated portfolios
    fig.add_trace(go.Scatter(
        x=results[1,:], y=results[0,:],
        mode='markers',
        marker=dict(color=results[2,:], colorscale='Viridis', showscale=True, size=5),
        name='Simulated Portfolios'
    ))

    # 2. Highlight the Maximum Sharpe Ratio Portfolio (The "Best" balance)
    fig.add_trace(go.Scatter(
        x=[sdp], y=[rp],
        mode='markers',
        marker=dict(color='red', size=15, symbol='star'),
        name='Max Sharpe Ratio'
    ))

    fig.update_layout(
        title='Efficient Frontier: Monte Carlo Simulation',
        xaxis_title='Annualized Volatility (Risk)',
        yaxis_title='Annualized Return',
        template='plotly_white'
    )

    # Convert to HTML for Flask
    graph_html = fig.to_html(full_html=False)

    return graph_html
