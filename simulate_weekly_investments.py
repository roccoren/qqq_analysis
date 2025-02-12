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

# Generate line chart and analysis table
def analyze_and_visualize(data):
    investments = simulate_weekly_investments(data)
    total_investment = investments['Investment'].sum()
    final_portfolio_value = investments['Portfolio Value'].iloc[-1]
    total_profit = final_portfolio_value - total_investment
    annualized_return = ((final_portfolio_value / total_investment) ** (1 / 5)) - 1

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
    fund_code = "006479"  # Fund code
    data = fetch_fund_data(fund_code)  # Fetch 5 years of data
    if data is not None:
        print("Data fetched successfully. Starting simulation...")
        analysis_table = analyze_and_visualize(data)
        print("Analysis Table:")
        print(analysis_table)
    else:
        print("Failed to fetch data.")