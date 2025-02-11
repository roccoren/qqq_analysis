# QQQ Investment Strategy Analysis

This project analyzes different investment strategies for the QQQ ETF (NASDAQ-100 Index) by comparing the performance of investing at different times of the trading day (opening, closing, and average prices) across different weekdays.

## Features

- Fetches 5-year historical data for QQQ using yfinance
- Simulates $10,000 investments on different weekdays
- Compares three investment strategies:
  - Opening price strategy
  - Closing price strategy
  - Average price strategy (using daily high and low prices)
- Visualizes portfolio values over time
- Calculates and displays detailed performance metrics:
  - Total investment
  - Final value
  - Profit
  - Profit ratio
  - Average purchase price
  - Strategy comparisons

## Requirements

- Python 3.x
- Required packages:
  - yfinance
  - pandas
  - numpy
  - matplotlib

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

Note: The project includes a requirements.txt file that specifies all necessary Python packages and their versions. This ensures consistent dependency management across different environments.

## Usage

Run the analysis script:
```bash
python qqq_analysis.py
```

The script will:
1. Download QQQ historical data
2. Perform investment strategy analysis
3. Display a plot comparing different strategies
4. Print detailed performance metrics for each strategy

## Output

- Interactive plot showing portfolio values over time for each strategy
- Detailed performance metrics including:
  - Investment amounts
  - Final values
  - Profits and profit ratios
  - Strategy comparisons

## License

This project is open source and available under the MIT License.