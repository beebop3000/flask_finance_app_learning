## https://stooq.com/q/d/?s=gme.us 
## GET A PLOTLY THING WORKING


import pandas as pd
import plotly.express as px


# Replace 'your_data.csv' with your file path or URL
df = pd.read_csv('data/aapl_us_d.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Display the first few rows to verify
print(df.info())


fig = px.line(df, x='Date', y='Close', title='Simple Time Series Plot')


fig.show()
