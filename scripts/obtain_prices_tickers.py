import pandas as pd
import os
import yfinance as yf

project_dir = os.getcwd()
stocks_dir = os.path.join(project_dir, 'data/sp500/stocks')
excel_file = os.path.join(project_dir, 'data_analysis/sp500_analysis.xlsx')
ideas_df = pd.read_excel(excel_file, sheet_name=0)

symbol_list = list(ideas_df['Symbol'])

# Ensure the directory exists
os.makedirs(stocks_dir, exist_ok=True)

for symbol in symbol_list:
    # Download historical data for each symbol
    data = yf.download(symbol, start="2016-01-01", end="2025-01-01")
    data.index = data.index.strftime('%Y-%m-%d')
    data.reset_index(inplace=True)
    data.rename(columns={"Price": "Date"}, inplace=True) 
    
    file_path = os.path.join(stocks_dir, f"{symbol}.csv")
    data.to_csv(file_path, index=False)

print(ideas_df)
