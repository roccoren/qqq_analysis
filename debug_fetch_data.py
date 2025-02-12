import sys
from pathlib import Path

# Add the Ashare directory to the Python path
sys.path.append(str(Path(__file__).parent / "Ashare"))
from Ashare import get_price  # Importing the Ashare library

# Debugging the fetch_data function
if __name__ == "__main__":
    test_codes = ["006479", "000001.XSHG", "sh600519"]  # Test with multiple codes
    frequency = "1d"  # Daily data
    count = 5  # Fetch 5 days of data for debugging

    for code in test_codes:
        print(f"Testing with fund/stock code: {code}")
        try:
            data = get_price(code, frequency=frequency, count=count)
            print("Data type:", type(data))  # Print the type of the returned data
            print("Data content:", data)  # Print the full content of the data
        except Exception as e:
            print(f"Error for code {code}: {e}")