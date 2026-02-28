from flask import Flask, render_template, request
import pandas as pd


from indicator_tools import movingAverage, plotChart
from trading_algo import trading_algo

# I want to build out some features like a moving average slider.
# Build a trading strategy.
# Build a ledger to keep track of the profit and loss.



app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():

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

                
    
    
    return render_template('index.html',
                            plot=graph_html,
                            ticker=ticker,
                            short_day_range=short_day_range, 
                            long_day_range = long_day_range,
                            table_html=df_html)


if __name__ == "__main__":
    app.run(debug=True)
