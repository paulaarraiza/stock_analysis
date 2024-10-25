import pandas as pd
import os
import yfinance as yf

"""This function obtains fundamentals for all elements in a given .csv file
Will look unther the Symbol column. 
"""

# Set the directory path
project_dir = os.getcwd()
sp500_dir = os.path.join(project_dir, 'data/sp500')
scripts_dir = os.path.join(project_dir, 'scripts')

metadata_path = os.path.join(sp500_dir, 'metadata.csv')
metadata_df = pd.read_csv(metadata_path)
symbol_list = list(metadata_df['Symbol'])

indicator_types = [
    "Fundamental", "Technical", "Company Info", "Irrelevant"
]

yfin_indicators_df = pd.read_csv(os.path.join(scripts_dir, 'yfinance_indicators.csv'), sep=";")


# Define categories
fundamental_indicators = yfin_indicators_df[yfin_indicators_df['Category'] == 'Fundamental']['Indicator'].tolist()
technical_indicators = yfin_indicators_df[yfin_indicators_df['Category'] == 'Technical']['Indicator'].tolist()
company_indicators = yfin_indicators_df[yfin_indicators_df['Category'] == 'Company Info']['Indicator'].tolist()

# Initialize lists to store data for each category
fundamentals_data = []
technical_data = []
company_data = []

# Loop through each symbol and retrieve data
for symbol in symbol_list:
    stock = yf.Ticker(symbol)
    fundamentals = stock.info  # Get the stock's fundamental data
    
    # Filter the fundamentals dictionary for each category
    fundamental_values = {key: fundamentals.get(key, None) for key in fundamental_indicators}
    technical_values = {key: fundamentals.get(key, None) for key in technical_indicators}
    company_values = {key: fundamentals.get(key, None) for key in company_indicators}
    
    # Add the symbol to each category data for identification
    fundamental_values['Symbol'] = symbol
    technical_values['Symbol'] = symbol
    company_values['Symbol'] = symbol
    
    # Append data to each list
    fundamentals_data.append(fundamental_values)
    technical_data.append(technical_values)
    company_data.append(company_values)

# Convert the lists into DataFrames and save them
fundamental_df = pd.DataFrame(fundamentals_data)
technical_df = pd.DataFrame(technical_data)
company_df = pd.DataFrame(company_data)

fundamental_df.to_csv(os.path.join(sp500_dir, 'fundamental.csv'), index=False)
technical_df.to_csv(os.path.join(sp500_dir, 'technical.csv'), index=False)
company_df.to_csv(os.path.join(sp500_dir, 'company.csv'), index=False)
