from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from data_fetch import get_stock_data, get_market_analysis
from llm_handler import process_query
from analytics import analyze_trends

app = FastAPI(title="Stock Market Analysis API")

# Enable CORS with more specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class StockQuery(BaseModel):
    symbol: str
    query: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Stock Market Analysis API is running"}

@app.get("/test-connection")
async def test_connection():
    return {"status": "success", "message": "Backend is connected!"}

@app.post("/analyze")
async def analyze_stock(stock_query: StockQuery):
    try:
        print(f"Received request for symbol: {stock_query.symbol}")
        
        # Fetch stock data
        stock_data = get_stock_data(stock_query.symbol)
        if not stock_data:
            raise HTTPException(status_code=404, detail="Stock data not found")

        # Get market analysis
        market_analysis = get_market_analysis(stock_query.symbol)

        # Process query and get insights
        analysis_result = process_query(stock_query.query, stock_data)

        # Get trends
        trends = analyze_trends(stock_data)

        return {
            "stock_data": stock_data.to_dict(),
            "market_analysis": market_analysis,
            "analysis": analysis_result,
            "trends": trends
        }

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 