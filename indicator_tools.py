import plotly.express as px



def movingAverage(df, days):
    return df['Close'].rolling(window=days).mean()


def plotChart(df):
    fig = px.line(df, x='Date', y=['Close','short_average','long_average'], title='Simple Time Series Plot')
    fig.update_layout(height=800, width = 1600)
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return graph_html