import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add the Ashare directory to the Python path
sys.path.append(str(Path(__file__).parent / "Ashare"))
from Ashare import get_price  # Importing the Ashare library

# Fetch historical data for the fund
def fetch_data(fund_code, frequency, count, end_date=None):
    data = get_price(fund_code, frequency=frequency, count=count, end_date=end_date)
    print("Data type:", type(data))  # Debugging: Print the type of the returned data
    print("Data content:", data)  # Debugging: Print the full content of the data
    if isinstance(data, pd.DataFrame) and not data.empty:
        return data
    elif isinstance(data, list):
        print("Data is a list. Converting to DataFrame...")
        # Attempt to convert list to DataFrame
        try:
            data = pd.DataFrame(data, columns=["date", "open", "close", "high", "low", "volume"])
            data["date"] = pd.to_datetime(data["date"])
            data.set_index("date", inplace=True)
            return data
        except Exception as e:
            raise ValueError(f"Failed to convert list to DataFrame: {e}")
    else:
        raise ValueError("No valid data found for the specified fund code and date range.")

# Simulate a 5-year weekday investment strategy
def simulate_strategy(data):
    # Example strategy: Buy on Mondays, sell on Fridays
    data['Weekday'] = data.index.weekday
    data['Signal'] = np.where(data['Weekday'] == 0, 1, 0)  # Buy on Monday
    data['Signal'] = np.where(data['Weekday'] == 4, -1, data['Signal'])  # Sell on Friday
    data['Position'] = data['Signal'].cumsum()
    data['Daily Return'] = data['close'].pct_change()
    data['Strategy Return'] = data['Position'].shift(1) * data['Daily Return']
    return data

# Generate line chart data
def generate_chart(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['close'], label='Close Price')
    plt.plot((1 + data['Strategy Return']).cumprod(), label='Strategy Performance')
    plt.title('Market Trends and Strategy Performance')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid()
    plt.show()

# Main function
if __name__ == "__main__":
    fund_code = "006479"  # Fund code
    frequency = "1d"  # Daily data
    count = 1250  # Approx. 5 years of data (250 trading days per year)

    try:
        # Step 1: Fetch data
        data = fetch_data(fund_code, frequency, count)
        print("Data fetched successfully.")

        # Step 2: Simulate strategy
        data = simulate_strategy(data)
        print("Strategy simulation completed.")

        # Step 3: Generate chart
        generate_chart(data)
        print("Chart generated successfully.")

        # Step 4: Analyze performance
        total_profit = (1 + data['Strategy Return']).prod() - 1
        annualized_return = (1 + total_profit) ** (1 / 5) - 1
        volatility = data['Strategy Return'].std() * np.sqrt(252)
        print(f"Total Profit: {total_profit:.2%}")
        print(f"Annualized Return: {annualized_return:.2%}")
        print(f"Volatility: {volatility:.2%}")

    except Exception as e:
        print(f"Error: {e}")