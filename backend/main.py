from flask import Flask, request, jsonify
from flask_cors import CORS
from data_fetch import get_stock_data, get_market_analysis
from llm_handler import process_query
from analytics import analyze_trends
import traceback

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def root():
    return jsonify({"message": "Stock Market Analysis API is running"})

@app.route('/test-connection')
def test_connection():
    return jsonify({"status": "success", "message": "Backend is connected!"})

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        symbol = data.get('symbol')
        query = data.get('query')
        
        if not symbol:
            return jsonify({"error": "Stock symbol is required"}), 400
            
        print(f"Received request for symbol: {symbol}")
        
        # Fetch stock data
        try:
            stock_data = get_stock_data(symbol)
            if stock_data is None or stock_data.empty:
                return jsonify({"error": "No stock data found for the given symbol"}), 404
        except Exception as e:
            print(f"Error fetching stock data: {str(e)}")
            return jsonify({"error": f"Failed to fetch stock data: {str(e)}"}), 500

        # Get market analysis
        try:
            market_analysis = get_market_analysis(symbol)
        except Exception as e:
            print(f"Error fetching market analysis: {str(e)}")
            market_analysis = {"error": "Failed to fetch market analysis"}

        # Process query and get insights
        try:
            analysis_result = process_query(query, stock_data)
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            analysis_result = "Failed to generate analysis"

        # Get trends
        try:
            trends = analyze_trends(stock_data)
        except Exception as e:
            print(f"Error analyzing trends: {str(e)}")
            trends = {"error": "Failed to analyze trends"}

        # Convert DataFrame to dict with string dates as keys
        stock_data_dict = {}
        for date in stock_data.index:
            stock_data_dict[date.strftime('%Y-%m-%d')] = stock_data.loc[date].to_dict()

        return jsonify({
            "stock_data": stock_data_dict,
            "market_analysis": market_analysis,
            "analysis": analysis_result,
            "trends": trends
        })

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000) 