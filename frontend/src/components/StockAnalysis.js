import React, { useState } from 'react';

function StockAnalysis({ onAnalyze }) {
  const [symbol, setSymbol] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (symbol.trim()) {
      onAnalyze(symbol.toUpperCase());
    }
  };

  return (
    <div className="stock-analysis">
      <h2>Stock Analysis</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="symbol">Stock Symbol:</label>
          <input
            type="text"
            id="symbol"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="Enter stock symbol (e.g., AAPL)"
            required
          />
        </div>
        <button type="submit">Analyze Stock</button>
      </form>
    </div>
  );
}

export default StockAnalysis; 