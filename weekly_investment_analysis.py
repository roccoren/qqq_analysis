import pandas as pd
import matplotlib.pyplot as plt
from fetch_eastmoney_data import fetch_fund_data

# Simulate weekly investments every 7 days
def simulate_weekly_investments(data, investment_amount=100):
    investment_dates = data.iloc[::7].index  # Select every 7th day
    investments = pd.DataFrame(index=investment_dates)
    investments['Investment'] = investment_amount
    investments['Units'] = investments['Investment'] / data.loc[investment_dates, 'netWorth']
    investments['Cumulative Units'] = investments['Units'].cumsum()
    investments['Portfolio Value'] = investments['Cumulative Units'] * data.loc[investment_dates, 'netWorth']
    return investments

# Analyze and visualize weekly investments
def analyze_and_visualize(data):
    investments = simulate_weekly_investments(data)
    total_investment = investments['Investment'].sum()
    final_portfolio_value = investments['Portfolio Value'].iloc[-1]
    total_profit = final_portfolio_value - total_investment
    annualized_return = ((final_portfolio_value / total_investment) ** (1 / (len(data) / 252))) - 1

    # Generate line chart
    plt.figure(figsize=(12, 6))
    plt.plot(investments.index, investments['Portfolio Value'], label="Portfolio Value")
    plt.title("Portfolio Growth for Weekly Investments")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (CNY)")
    plt.legend()
    plt.grid()
    plt.show()

    # Create analysis table
    analysis_table = pd.DataFrame({
        "Total Investment": [total_investment],
        "Final Portfolio Value": [final_portfolio_value],
        "Total Profit": [total_profit],
        "Annualized Return": [annualized_return]
    })
    return analysis_table

if __name__ == "__main__":
    fund_code = "021778"  # Fund code
    start_date = "2024-08-20"  # Start date for analysis
    data = fetch_fund_data(fund_code, start_date)  # Fetch data from start_date
    if data is not None:
        print("Data fetched successfully. Starting analysis...")
        analysis_table = analyze_and_visualize(data)
        print("Analysis Table:")
        print(analysis_table)
    else:
        print("Failed to fetch data.")