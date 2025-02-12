import requests
import pandas as pd

# Fetch historical data for the fund using Eastmoney API
def fetch_fund_data(fund_code, start_date=None):
    url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        
        # Parse the response to extract historical data
        # The data is embedded in JavaScript; we need to extract and process it
        content = response.text
        start = content.find("Data_netWorthTrend") + len("Data_netWorthTrend") + 3
        end = content.find(";", start)
        json_data = eval(content[start:end])  # Convert JavaScript array to Python list
        
        # Convert to DataFrame
        data = pd.DataFrame(json_data)
        data['date'] = pd.to_datetime(data['x'], unit='ms')
        data['netWorth'] = data['y']
        data = data[['date', 'netWorth']]
        data.set_index('date', inplace=True)
        
        # Filter for data starting from `start_date` if specified
        if start_date:
            data = data[data.index >= pd.Timestamp(start_date)]
        return data
    except Exception as e:
        print(f"Error fetching data for fund code {fund_code}: {e}")
        return None

if __name__ == "__main__":
    fund_code = "005698"  # Fund code
    start_date = "2024-08-20"  # Start date for fetching data
    output_file = "fund_005698_data.csv"  # Output CSV file
    data = fetch_fund_data(fund_code, start_date)
    if data is not None:
        print(f"Data from {start_date} to date fetched successfully. Saving to {output_file}...")
        data.to_csv(output_file)
        print(f"Data saved to {output_file}.")
    else:
        print("Failed to fetch data.")