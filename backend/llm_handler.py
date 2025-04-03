import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()


DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

def format_stock_data(stock_data):
    """Format stock data for analysis"""
    if isinstance(stock_data, pd.DataFrame):
        return stock_data.to_string()
    return str(stock_data)

def process_query(query, stock_data):
    """Process the query using DeepSeek"""
    try:
       
        formatted_data = format_stock_data(stock_data)
        system_message = """You are a financial analyst expert. Analyze the given stock data and provide insights."""
        
        user_message = f"""
        Stock Data:
        {formatted_data}
        
        Question: {query if query else 'Provide a general analysis of this stock data.'}
        """
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-ai/DeepSeek-V3-0324",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        # Make the API call
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        # Check for errors
        if response.status_code != 200:
            error_data = response.json()
            raise Exception(f"DeepSeek API Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
        
        # Extract and return the analysis
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"Error in process_query: {str(e)}")
        return f"Error processing query: {str(e)}" 