import React from 'react';

function ResultsDisplay({ analysis, loading, error }) {
  if (loading) {
    return <div className="loading">Loading analysis...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (!analysis) {
    return null;
  }

  return (
    <div className="results-display">
      <h2>Analysis Results</h2>
      
      <section className="stock-data">
        <h3>Stock Data</h3>
        <div className="data-grid">
          <div className="data-item">
            <span className="label">Current Price:</span>
            <span className="value">${analysis.stock_data['4. close'][0].toFixed(2)}</span>
          </div>
          <div className="data-item">
            <span className="label">Volume:</span>
            <span className="value">{analysis.stock_data['5. volume'][0].toLocaleString()}</span>
          </div>
          <div className="data-item">
            <span className="label">High:</span>
            <span className="value">${analysis.stock_data['2. high'][0].toFixed(2)}</span>
          </div>
          <div className="data-item">
            <span className="label">Low:</span>
            <span className="value">${analysis.stock_data['3. low'][0].toFixed(2)}</span>
          </div>
        </div>
      </section>

      <section className="market-analysis">
        <h3>Market Analysis</h3>
        {analysis.market_analysis && (
          <div className="analysis-content">
            {analysis.market_analysis.data.map((symbolData, index) => (
              <div key={index} className="symbol-analysis">
                <h4>{symbolData.symbol}</h4>
                <ul>
                  {symbolData.calculations.map((calc, calcIndex) => (
                    <li key={calcIndex}>
                      {calc.name}: {calc.value}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="trends">
        <h3>Trends</h3>
        <div className="trends-content">
          <div className="trend-item">
            <span className="label">Price Change:</span>
            <span className={`value ${analysis.trends.price_change.percentage >= 0 ? 'positive' : 'negative'}`}>
              {analysis.trends.price_change.percentage}%
            </span>
          </div>
          <div className="trend-item">
            <span className="label">Volume Trend:</span>
            <span className="value">{analysis.trends.volume_analysis.trend}</span>
          </div>
          <div className="trend-item">
            <span className="label">Volatility:</span>
            <span className="value">{analysis.trends.volatility}%</span>
          </div>
          <div className="trend-item">
            <span className="label">Support Level:</span>
            <span className="value">${analysis.trends.support_resistance.support}</span>
          </div>
          <div className="trend-item">
            <span className="label">Resistance Level:</span>
            <span className="value">${analysis.trends.support_resistance.resistance}</span>
          </div>
        </div>
      </section>

      <section className="ai-analysis">
        <h3>AI Analysis</h3>
        <div className="analysis-content">
          {analysis.analysis}
        </div>
      </section>
    </div>
  );
}

export default ResultsDisplay; 