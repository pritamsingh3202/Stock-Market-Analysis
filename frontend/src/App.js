import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [symbol, setSymbol] = useState('');
  const [query, setQuery] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('checking');

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/test-connection');
      if (response.ok) {
        setConnectionStatus('connected');
      } else {
        setConnectionStatus('error');
      }
    } catch (err) {
      setConnectionStatus('error');
      console.error('Connection test failed:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      if (!symbol.trim()) {
        throw new Error('Please enter a stock symbol');
      }

      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol: symbol.trim(), query: query.trim() }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Analysis request failed');
      }

      setAnalysis(data);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatStockData = (stockData) => {
    if (!stockData) return null;
    
    const dates = Object.keys(stockData).sort().reverse();
    return dates.map(date => ({
      date,
      ...stockData[date]
    }));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Stock Market Analysis</h1>
        <div className={`connection-status ${connectionStatus}`}>
          {connectionStatus === 'connected' && 'Backend Connected'}
          {connectionStatus === 'error' && 'Backend Connection Error'}
          {connectionStatus === 'checking' && 'Checking Backend Connection...'}
        </div>
      </header>

      <main>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="symbol">Stock Symbol:</label>
            <input
              type="text"
              id="symbol"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="Enter stock symbol (e.g., AAPL)"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="query">Analysis Query (Optional):</label>
            <input
              type="text"
              id="query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your question about the stock"
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Stock'}
          </button>
        </form>

        {error && (
          <div className="error">
            <h3>Error</h3>
            <p>{error}</p>
            <p className="error-tip">Please check if:</p>
            <ul>
              <li>The stock symbol is correct</li>
              <li>You have a valid Alpha Vantage API key</li>
              <li>The backend server is running</li>
            </ul>
          </div>
        )}

        {analysis && (
          <div className="analysis-results">
            <h2>Analysis Results</h2>
            
            <div className="section">
              <h3>Market Analysis</h3>
              <pre>{JSON.stringify(analysis.market_analysis, null, 2)}</pre>
            </div>

            <div className="section">
              <h3>Stock Data</h3>
              <div className="stock-data-table">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Open</th>
                      <th>High</th>
                      <th>Low</th>
                      <th>Close</th>
                      <th>Volume</th>
                    </tr>
                  </thead>
                  <tbody>
                    {formatStockData(analysis.stock_data)?.map((row, index) => (
                      <tr key={index}>
                        <td>{row.date}</td>
                        <td>${parseFloat(row['1. open']).toFixed(2)}</td>
                        <td>${parseFloat(row['2. high']).toFixed(2)}</td>
                        <td>${parseFloat(row['3. low']).toFixed(2)}</td>
                        <td>${parseFloat(row['4. close']).toFixed(2)}</td>
                        <td>{parseInt(row['5. volume']).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="section">
              <h3>Trends</h3>
              <pre>{JSON.stringify(analysis.trends, null, 2)}</pre>
            </div>

            {analysis.analysis && (
              <div className="section">
                <h3>AI Analysis</h3>
                <p>{analysis.analysis}</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 