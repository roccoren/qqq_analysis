import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Fetch QQQ data for the last 5 years
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)
qqq = yf.download('QQQ', start=start_date, end=end_date)

# Create a copy of the data for analysis
df = qqq.copy()

# Add day of week column
df['DayOfWeek'] = df.index.dayofweek

# Initialize investment columns for all weekday strategies
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
for day in weekdays:
    # Opening price strategy columns
    df[f'{day}_Open_Investment'] = 0.0
    df[f'{day}_Open_Shares'] = 0.0
    df[f'{day}_Open_Value'] = 0.0
    # Closing price strategy columns
    df[f'{day}_Close_Investment'] = 0.0
    df[f'{day}_Close_Shares'] = 0.0
    df[f'{day}_Close_Value'] = 0.0
    # Average price strategy columns
    df[f'{day}_Avg_Investment'] = 0.0
    df[f'{day}_Avg_Shares'] = 0.0
    df[f'{day}_Avg_Value'] = 0.0

# Initialize tracking variables
open_investments = {day: 0.0 for day in weekdays}
open_shares = {day: 0.0 for day in weekdays}
close_investments = {day: 0.0 for day in weekdays}
close_shares = {day: 0.0 for day in weekdays}
avg_investments = {day: 0.0 for day in weekdays}
avg_shares = {day: 0.0 for day in weekdays}

# Simulate $10,000 investment for each strategy
for idx in range(len(df)):
    current_day = df['DayOfWeek'].iloc[idx]
    open_price = float(df['Open'].iloc[idx])
    close_price = float(df['Close'].iloc[idx])
    high_price = float(df['High'].iloc[idx])
    low_price = float(df['Low'].iloc[idx])
    avg_price = (high_price + low_price) / 2
    
    if np.isnan(open_price) or np.isnan(close_price) or np.isnan(avg_price):
        continue
        
    if current_day < 5:  # Monday (0) through Friday (4)
        day_name = weekdays[current_day]
        investment = 10000.0
        
        # Opening price strategy
        new_open_shares = investment / open_price
        open_shares[day_name] += new_open_shares
        open_investments[day_name] += investment
        
        # Closing price strategy
        new_close_shares = investment / close_price
        close_shares[day_name] += new_close_shares
        close_investments[day_name] += investment

        # Average price strategy
        new_avg_shares = investment / avg_price
        avg_shares[day_name] += new_avg_shares
        avg_investments[day_name] += investment
    
    # Update all daily values
    for day in weekdays:
        # Update opening price strategy values
        df.loc[df.index[idx], f'{day}_Open_Investment'] = open_investments[day]
        df.loc[df.index[idx], f'{day}_Open_Shares'] = open_shares[day]
        df.loc[df.index[idx], f'{day}_Open_Value'] = open_shares[day] * close_price
        
        # Update closing price strategy values
        df.loc[df.index[idx], f'{day}_Close_Investment'] = close_investments[day]
        df.loc[df.index[idx], f'{day}_Close_Shares'] = close_shares[day]
        df.loc[df.index[idx], f'{day}_Close_Value'] = close_shares[day] * close_price

        # Update average price strategy values
        df.loc[df.index[idx], f'{day}_Avg_Investment'] = avg_investments[day]
        df.loc[df.index[idx], f'{day}_Avg_Shares'] = avg_shares[day]
        df.loc[df.index[idx], f'{day}_Avg_Value'] = avg_shares[day] * close_price

# Create the plot
plt.figure(figsize=(15, 8))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
for i, day in enumerate(weekdays):
    plt.plot(df.index, df[f'{day}_Open_Value'].ffill(), label=f'{day} Open', color=colors[i], linestyle='-')
    plt.plot(df.index, df[f'{day}_Close_Value'].ffill(), label=f'{day} Close', color=colors[i], linestyle='--')
    plt.plot(df.index, df[f'{day}_Avg_Value'].ffill(), label=f'{day} Avg', color=colors[i], linestyle=':')

plt.title('QQQ Investment Strategy Comparison - Opening vs Closing vs Average Prices')
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# Calculate and display results
print("\nResults:")
for day in weekdays:
    # Opening price strategy results
    open_final_value = df[f'{day}_Open_Value'].ffill().iloc[-1]
    open_total_investment = df[f'{day}_Open_Investment'].fillna(0).iloc[-1]
    open_profit = open_final_value - open_total_investment
    open_profit_ratio = (open_profit / open_total_investment) * 100 if open_total_investment > 0 else 0
    open_avg_price = open_total_investment / open_shares[day] if open_shares[day] > 0 else 0
    
    # Closing price strategy results
    close_final_value = df[f'{day}_Close_Value'].ffill().iloc[-1]
    close_total_investment = df[f'{day}_Close_Investment'].fillna(0).iloc[-1]
    close_profit = close_final_value - close_total_investment
    close_profit_ratio = (close_profit / close_total_investment) * 100 if close_total_investment > 0 else 0
    close_avg_price = close_total_investment / close_shares[day] if close_shares[day] > 0 else 0

    # Average price strategy results
    avg_final_value = df[f'{day}_Avg_Value'].ffill().iloc[-1]
    avg_total_investment = df[f'{day}_Avg_Investment'].fillna(0).iloc[-1]
    avg_profit = avg_final_value - avg_total_investment
    avg_profit_ratio = (avg_profit / avg_total_investment) * 100 if avg_total_investment > 0 else 0
    avg_price = avg_total_investment / avg_shares[day] if avg_shares[day] > 0 else 0
    
    print(f"\n{day} Strategy:")
    print(f"Opening Price Strategy:")
    print(f"  Total Investment: ${open_total_investment:,.2f}")
    print(f"  Final Value: ${open_final_value:,.2f}")
    print(f"  Profit: ${open_profit:,.2f}")
    print(f"  Profit Ratio: {open_profit_ratio:.2f}%")
    print(f"  Average Price: ${open_avg_price:.2f}")
    
    print(f"Closing Price Strategy:")
    print(f"  Total Investment: ${close_total_investment:,.2f}")
    print(f"  Final Value: ${close_final_value:,.2f}")
    print(f"  Profit: ${close_profit:,.2f}")
    print(f"  Profit Ratio: {close_profit_ratio:.2f}%")
    print(f"  Average Price: ${close_avg_price:.2f}")

    print(f"Average Price Strategy:")
    print(f"  Total Investment: ${avg_total_investment:,.2f}")
    print(f"  Final Value: ${avg_final_value:,.2f}")
    print(f"  Profit: ${avg_profit:,.2f}")
    print(f"  Profit Ratio: {avg_profit_ratio:.2f}%")
    print(f"  Average Price: ${avg_price:.2f}")
    
    # Calculate and display the differences
    print(f"Strategy Comparisons:")
    print(f"  Open vs Close: {open_profit_ratio - close_profit_ratio:.2f}%")
    print(f"  Open vs Avg: {open_profit_ratio - avg_profit_ratio:.2f}%")
    print(f"  Close vs Avg: {close_profit_ratio - avg_profit_ratio:.2f}%")

plt.show()