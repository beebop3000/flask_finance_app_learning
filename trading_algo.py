# takes a time serires df
# sets profit to 0
# sets holding to false
# trade dict to empty
# when short crosses over long buy
            # holding goes to true
            # record time and purchasing price
# when short dips below long sell
            # holding goes to false
            # recod time and purchasing price
# calculate profit and loss
# add this as one record to dictionary
# display this table under the chart

import pandas as pd

def trading_algo(df):
    total_profit = 0
    holding = False
    
    # Use a list to collect results - much faster than modifying objects in loops
    trade_list = []
    
    # Store purchase info temporarily
    p_date, p_price = None, None

    for row in df.itertuples():
        # Check for None/NaN safely
        if pd.isna(row.short_average) or pd.isna(row.long_average):
            continue

        # Logic For Purchase
        if row.short_average > row.long_average and not holding:
            p_date = row.Date
            p_price = row.Close
            holding = True
        
        # Logic For Sale
        elif row.short_average < row.long_average and holding:
            trade_profit = row.Close - p_price
            total_profit += trade_profit

            trade_list.append({
                'purchase_date': p_date,
                'purchase_price': p_price,
                'selling_date': row.Date,
                'selling_price': row.Close,
                'trade_profit': trade_profit,
                'total_profit': total_profit
            })
            holding = False

    # Create the final DataFrame ONCE at the very end
    return pd.DataFrame(trade_list)



