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
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol, query }),
      });

      if (!response.ok) {
        throw new Error('Analysis request failed');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
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

        {error && <div className="error">{error}</div>}

        {analysis && (
          <div className="analysis-results">
            <h2>Analysis Results</h2>
            
            <div className="section">
              <h3>Market Analysis</h3>
              <pre>{JSON.stringify(analysis.market_analysis, null, 2)}</pre>
            </div>

            <div className="section">
              <h3>Stock Data</h3>
              <pre>{JSON.stringify(analysis.stock_data, null, 2)}</pre>
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