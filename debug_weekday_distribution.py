import pandas as pd
from fetch_eastmoney_data import fetch_fund_data

# Debugging weekday distribution in the data
if __name__ == "__main__":
    fund_code = "006479"  # Fund code
    data = fetch_fund_data(fund_code)  # Fetch 5 years of data
    if data is not None:
        print("Data fetched successfully. Analyzing weekday distribution...")
        data['Weekday'] = data.index.weekday
        weekday_counts = data['Weekday'].value_counts().sort_index()
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for i, count in weekday_counts.items():
            print(f"{weekday_names[i]}: {count} entries")
    else:
        print("Failed to fetch data.")