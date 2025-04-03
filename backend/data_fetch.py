import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

def get_stock_data(symbol):
    try:
        if not ALPHAVANTAGE_API_KEY:
            raise ValueError("Alpha Vantage API key is not set in environment variables")
            
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}'
        
        print(f"Fetching stock data from: {url}")
        
        # Make the API request
        response = requests.get(url)
        response.raise_for_status() 
        
        data = response.json()
        
        if 'Error Message' in data:
            raise ValueError(f"Alpha Vantage API Error: {data['Error Message']}")
            
        if 'Note' in data:
            print(f"API Note: {data['Note']}")
            
        if 'Time Series (Daily)' not in data:
            raise ValueError(f"Invalid API response format: {json.dumps(data)}")
            
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        
        if df.empty:
            raise ValueError("No data returned from API")
         
         
        for column in df.columns:
            df[column] = pd.to_numeric(df[column])
      
        df.index = pd.to_datetime(df.index)
      
        df = df.sort_index(ascending=False)
        
        print(f"Successfully fetched {len(df)} days of stock data")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching stock data: {str(e)}")
        raise Exception(f"Failed to fetch stock data: {str(e)}")
    except Exception as e:
        print(f"Error in get_stock_data: {str(e)}")
        raise Exception(f"Error fetching stock data: {str(e)}")

def get_market_analysis(symbol):
    try:
        if not ALPHAVANTAGE_API_KEY:
            raise ValueError("Alpha Vantage API key is not set in environment variables")
            
        # Alpha Vantage API endpoint for running analytics
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}'
        
        print(f"Fetching market analysis from: {url}")
        
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  
        
        data = response.json()
        
        if 'Error Message' in data:
            raise ValueError(f"Alpha Vantage API Error: {data['Error Message']}")
            
        if 'Note' in data:
            print(f"API Note: {data['Note']}")
            
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching market analysis: {str(e)}")
        raise Exception(f"Failed to fetch market analysis: {str(e)}")
    except Exception as e:
        print(f"Error in get_market_analysis: {str(e)}")
        raise Exception(f"Error fetching market analysis: {str(e)}") 