import pandas as pd
import os
import yfinance as yf

project_dir = os.getcwd()
stocks_dir = os.path.join(project_dir, 'data/sp500/stocks')
excel_file = os.path.join(project_dir, 'data_analysis/sp500_analysis.xlsx')
ideas_df = pd.read_excel(excel_file, sheet_name=0)

symbol_list = list(ideas_df['Symbol'])

# Ensure the directory exists
excel_file_path = os.path.join(stocks_dir, 'all_symbols_data.xlsx')

# Define the fields to load
fields = [
    'dividendRate', 'dividendYield', 'exDividendDate', 'payoutRatio', 'fiveYearAvgDividendYield', 'beta',
    'trailingPE', 'forwardPE', 'marketCap', 'priceToSalesTrailing12Months', 'trailingAnnualDividendRate',
    'trailingAnnualDividendYield', 'enterpriseValue', 'profitMargins', 'dateShortInterest', 'shortRatio',
    'shortPercentOfFloat', 'bookValue', 'priceToBook', 'netIncomeToCommon', 'trailingEps', 'forwardEps',
    'enterpriseToRevenue', 'enterpriseToEbitda', 'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt',
    'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets',
    'returnOnEquity', 'freeCashflow', 'operatingCashflow', 'revenueGrowth', 'grossMargins', 'ebitdaMargins',
    'operatingMargins'
]

# Create an Excel writer to save multiple sheets in one file
with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    for symbol in symbol_list:
        # Download historical data and filter to only include 'Close' column
        historical_data = yf.download(symbol, start="2016-01-01", end="2025-01-01")[['Close']]
        
        # Format the date index to YYYY-MM-DD and reset it as a column
        historical_data.index = historical_data.index.strftime('%Y-%m-%d')
        historical_data.reset_index(inplace=True)
        
        # Rename the date column to 'Date'
        historical_data.rename(columns={"Price": "Date"}, inplace=True)
        
        # Get additional fundamental data
        stock_info = yf.Ticker(symbol).info
        fundamentals_data = {field: stock_info.get(field) for field in fields}
        
        # Expand fundamentals to match the number of rows in historical data
        fundamentals_df = pd.DataFrame([fundamentals_data] * len(historical_data), index=historical_data.index)
        
        # Concatenate historical and fundamental data
        combined_df = pd.concat([historical_data, fundamentals_df], axis=1)
        
        # Write each combined DataFrame to a separate sheet named after the symbol
        combined_df.to_excel(writer, sheet_name=symbol, index=False)