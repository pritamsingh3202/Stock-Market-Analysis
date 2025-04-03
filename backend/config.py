import os
from dotenv import load_dotenv

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_ANALYTICS_URL = "https://alphavantageapi.co/timeseries/running_analytics"


STOCK_PREDICTOR_MODEL = "foduucom/stockmarket-future-prediction"
MARKET_ANALYZER_MODEL = "bhaskartripathi/GPT_Neo_Market_Analysis"


DEFAULT_RANGE = "2month"
DEFAULT_INTERVAL = "DAILY"
DEFAULT_WINDOW_SIZE = 20
DEFAULT_CALCULATIONS = ["MEAN", "STDDEV(annualized=True)"]



ERROR_MESSAGES = {
    "api_key_missing": "API key not found in environment variables",
    "data_fetch_error": "Error fetching data from API",
    "analysis_error": "Error during analysis",
    "model_error": "Error processing with model"
} 