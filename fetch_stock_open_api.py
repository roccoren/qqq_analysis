from stock_open_api import StockOpenApi

# Fetch historical data for the fund using stock-open-api
def fetch_fund_data(fund_code):
    api = StockOpenApi()
    try:
        # Fetch fund data
        data = api.get_fund_data(fund_code)
        print("Data fetched successfully:")
        print(data)
    except Exception as e:
        print(f"Error fetching data for fund code {fund_code}: {e}")

if __name__ == "__main__":
    fund_code = "006479"  # Fund code
    fetch_fund_data(fund_code)