import pandas as pd
import matplotlib.pyplot as plt

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
    weekday_mapping = {6: 'Sunday', 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday'}
    results = {}
    plt.figure(figsize=(12, 6))
    
    for weekday, weekday_name in weekday_mapping.items():
        investments = simulate_daily_investments(data, weekday)
        if investments.empty:
            print(f"No investment data available for {weekday_name}. Skipping...")
            continue
        
        total_investment = investments['Investment'].sum()
        final_portfolio_value = investments['Portfolio Value'].iloc[-1]
        total_profit = final_portfolio_value - total_investment
        profit_ratio = (total_profit / total_investment) * 100 if total_investment > 0 else 0
        
        results[weekday_name] = {
            'Total Investment': total_investment,
            'Final Portfolio Value': final_portfolio_value,
            'Total Profit': total_profit,
            'Profit Ratio': profit_ratio
        }
        
        plt.plot(investments.index, investments['Portfolio Value'], label=f"{weekday_name}")
    
    plt.title("Portfolio Growth for Daily Investments (Sunday to Thursday)")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (CNY)")
    plt.legend()
    plt.grid()
    plt.show()
    
    # Create analysis table
    analysis_table = pd.DataFrame(results).T
    return analysis_table

if __name__ == "__main__":
    input_file = "fund_005698_data.csv"  # Input CSV file
    data = pd.read_csv(input_file, parse_dates=['date'], index_col='date')  # Load dataset
    if not data.empty:
        print("Dataset loaded successfully. Starting analysis...")
        analysis_table = analyze_and_visualize(data)
        print("Analysis Table:")
        print(analysis_table)
    else:
        print("Dataset is empty. Please check the input file.")