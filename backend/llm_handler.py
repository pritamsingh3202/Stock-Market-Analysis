import os
from dotenv import load_dotenv
from transformers import pipeline
import requests

load_dotenv()

# Initialize Hugging Face models
stock_predictor = pipeline("text2text-generation", model="foduucom/stockmarket-future-prediction")
market_analyzer = pipeline("text2text-generation", model="bhaskartripathi/GPT_Neo_Market_Analysis")

def process_query(query, stock_data):
    try:
        # Format stock data for the model
        formatted_data = format_stock_data(stock_data)
        
        # Generate prediction using stock predictor
        prediction = stock_predictor(formatted_data + " " + query, max_length=100)
        
        # Generate market analysis
        analysis = market_analyzer(formatted_data + " " + query, max_length=200)
        
        return {
            "prediction": prediction[0]["generated_text"],
            "analysis": analysis[0]["generated_text"]
        }
        
    except Exception as e:
        raise Exception(f"Error processing query: {str(e)}")

def format_stock_data(stock_data):
    """Format stock data for LLM input"""
    try:
        latest_data = stock_data.iloc[0]
        formatted_data = f"""
        Current Price: ${latest_data['4. close']:.2f}
        Volume: {int(latest_data['5. volume']):,}
        High: ${latest_data['2. high']:.2f}
        Low: ${latest_data['3. low']:.2f}
        
        Recent Price History:
        {stock_data.head().to_string()}
        """
        return formatted_data
    except Exception as e:
        raise Exception(f"Error formatting stock data: {str(e)}") 