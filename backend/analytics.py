import pandas as pd
import numpy as np

def analyze_trends(stock_data):
    try:
        # Calculate basic trends
        latest_price = stock_data['4. close'].iloc[0]
        prev_price = stock_data['4. close'].iloc[1]
        price_change = latest_price - prev_price
        price_change_pct = (price_change / prev_price) * 100
        
        # Calculate volume trends
        latest_volume = stock_data['5. volume'].iloc[0]
        avg_volume = stock_data['5. volume'].mean()
        volume_trend = "Above Average" if latest_volume > avg_volume else "Below Average"
        
        # Calculate price volatility
        returns = stock_data['4. close'].pct_change()
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        
        # Identify support and resistance levels
        recent_highs = stock_data['2. high'].head(5)
        recent_lows = stock_data['3. low'].head(5)
        resistance = recent_highs.max()
        support = recent_lows.min()
        
        return {
            "price_change": {
                "absolute": round(price_change, 2),
                "percentage": round(price_change_pct, 2)
            },
            "volume_analysis": {
                "current": latest_volume,
                "average": round(avg_volume, 2),
                "trend": volume_trend
            },
            "volatility": round(volatility * 100, 2),  # Convert to percentage
            "support_resistance": {
                "support": round(support, 2),
                "resistance": round(resistance, 2)
            }
        }
        
    except Exception as e:
        raise Exception(f"Error analyzing trends: {str(e)}") 