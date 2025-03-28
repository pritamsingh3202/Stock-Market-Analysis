import React, { useState } from 'react';

function QueryInterface({ onQuery }) {
  const [query, setQuery] = useState('');
  const [symbol, setSymbol] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (symbol.trim() && query.trim()) {
      onQuery(symbol.toUpperCase(), query);
    }
  };

  return (
    <div className="query-interface">
      <h2>Ask Questions About the Stock</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="query-symbol">Stock Symbol:</label>
          <input
            type="text"
            id="query-symbol"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="Enter stock symbol (e.g., AAPL)"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="query">Your Question:</label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about the stock (e.g., What are the key trends and potential risks?)"
            required
          />
        </div>
        <button type="submit">Get AI Analysis</button>
      </form>
    </div>
  );
}

export default QueryInterface; 