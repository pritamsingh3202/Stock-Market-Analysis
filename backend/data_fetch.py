import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

def get_stock_data(symbol):
    try:
        # Alpha Vantage API endpoint for daily data
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}'
        
        # Make the API request
        response = requests.get(url)
        data = response.json()
        
        if 'Time Series (Daily)' not in data:
            raise ValueError(f"Error: {data.get('Note', 'Unknown error occurred')}")
            
        # Convert the data to a DataFrame
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        
        # Convert string values to float
        for column in df.columns:
            df[column] = pd.to_numeric(df[column])
            
        # Convert index to datetime
        df.index = pd.to_datetime(df.index)
        
        # Sort by date in descending order
        df = df.sort_index(ascending=False)
        
        return df
        
    except Exception as e:
        raise Exception(f"Error fetching stock data: {str(e)}")

def get_market_analysis(symbol):
    try:
        # Alpha Vantage API endpoint for running analytics
        url = f'https://alphavantageapi.co/timeseries/running_analytics?SYMBOLS={symbol}&RANGE=2month&INTERVAL=DAILY&OHLC=close&WINDOW_SIZE=20&CALCULATIONS=MEAN,STDDEV(annualized=True)&apikey={ALPHAVANTAGE_API_KEY}'
        
        # Make the API request
        response = requests.get(url)
        data = response.json()
        
        if 'Error Message' in data:
            raise ValueError(f"Error: {data['Error Message']}")
            
        return data
        
    except Exception as e:
        raise Exception(f"Error fetching market analysis: {str(e)}") 