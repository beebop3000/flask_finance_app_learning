from flask import Flask, render_template, request
import pandas as pd

from indicator_tools import movingAverage, plotChart
from trading_algo import trading_algo

from efficientFrontier import *





# I want to build out some features like a moving average slider.
# Build a trading strategy.
# Build a ledger to keep track of the profit and loss.

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/moving_average', methods=['GET', 'POST'])
def moving_average():

    ticker = "aapl_us_d" # Default ticker
    short_day_range = 30
    long_day_range = 90 

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        print(f"Selected ticker: {ticker}")

        short_slider_val = request.form.get('shortRange')
        if short_slider_val:
            short_day_range = int(short_slider_val)

        long_slider_val = request.form.get('longRange')
        if long_slider_val:
            long_day_range = int(long_slider_val)

    df = pd.read_csv(f'data/{ticker}.csv').tail(3*365)
    df['Date'] = pd.to_datetime(df['Date'])

    df['short_average'] = movingAverage(df,short_day_range)
    df['long_average'] = movingAverage(df,long_day_range)

    graph_html = plotChart(df)

    trade_df = trading_algo(df)

    df_html = trade_df.to_html(classes='dataframe', index=False)        
    
    return render_template('moving_average.html',
                            plot=graph_html,
                            ticker=ticker,
                            short_day_range=short_day_range, 
                            long_day_range = long_day_range,
                            table_html=df_html)


@app.route('/efficient_frontier')
def efficient_frontier():

    returns  = load_ef_files()
    results = ef_simulation(returns)
    graph_html = plot_ef(results)

    return render_template('efficient_frontier.html', plot=graph_html)


if __name__ == "__main__":
    app.run(debug=True)
