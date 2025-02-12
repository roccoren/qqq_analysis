import pandas as pd
import matplotlib.pyplot as plt
from fetch_eastmoney_data import fetch_fund_data

# Simulate daily investments for each weekday
def simulate_daily_investments(data, weekday, investment_amount=100):
    data['Weekday'] = data.index.weekday
    investment_dates = data[data['Weekday'] == weekday].index
    investments = pd.DataFrame(index=investment_dates)
    investments['Investment'] = investment_amount
    investments['Units'] = investments['Investment'] / data.loc[investment_dates, 'netWorth']
    investments['Cumulative Units'] = investments['Units'].cumsum()
    investments['Portfolio Value'] = investments['Cumulative Units'] * data.loc[investment_dates, 'netWorth']
    return investments

# Analyze and visualize daily investments
def analyze_and_visualize(data):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    results = {}
    plt.figure(figsize=(12, 6))
    
    for weekday in range(5):  # Monday (0) to Friday (4)
        investments = simulate_daily_investments(data, weekday)
        total_investment = investments['Investment'].sum()
        final_portfolio_value = investments['Portfolio Value'].iloc[-1]
        total_profit = final_portfolio_value - total_investment
        profit_ratio = (total_profit / total_investment) * 100 if total_investment > 0 else 0
        
        results[weekdays[weekday]] = {
            'Total Investment': total_investment,
            'Final Portfolio Value': final_portfolio_value,
            'Total Profit': total_profit,
            'Profit Ratio': profit_ratio
        }
        
        plt.plot(investments.index, investments['Portfolio Value'], label=f"{weekdays[weekday]}")
    
    plt.title("Portfolio Growth for Daily Investments by Weekday")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (CNY)")
    plt.legend()
    plt.grid()
    plt.show()
    
    # Create analysis table
    analysis_table = pd.DataFrame(results).T
    return analysis_table

if __name__ == "__main__":
    fund_code = "006479"  # Fund code
    data = fetch_fund_data(fund_code)  # Fetch 5 years of data
    if data is not None:
        print("Data fetched successfully. Starting analysis...")
        analysis_table = analyze_and_visualize(data)
        print("Analysis Table:")
        print(analysis_table)
    else:
        print("Failed to fetch data.")