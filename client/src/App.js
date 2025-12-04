import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [useTransformation, setUseTransformation] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/stats`);
      setStats(res.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await axios.post(`${API_BASE_URL}/api/query`, {
        query: query,
        use_transformation: useTransformation
      });
      setResponse(res.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process query');
    } finally {
      setLoading(false);
    }
  };

  const handleRebuild = async () => {
    if (!window.confirm('Rebuild vector store? This may take a few minutes.')) return;

    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/api/rebuild`);
      setStats(res.data.stats);
      alert('Vector store rebuilt successfully');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to rebuild');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>RAG-Powered Assistant</h1>
        <p>Query your document corpus using Retrieval-Augmented Generation</p>
      </header>

      <div className="container">
        <div className="stats-panel">
          {stats && (
            <div className="stats">
              <span>Chunks: {stats.total_chunks}</span>
              <span>Dimension: {stats.dimension}</span>
            </div>
          )}
          <button onClick={handleRebuild} className="rebuild-btn" disabled={loading}>
            Rebuild Index
          </button>
        </div>

        <form onSubmit={handleSubmit} className="query-form">
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={useTransformation}
                onChange={(e) => setUseTransformation(e.target.checked)}
              />
              Enable Query Transformation
            </label>
          </div>
          <div className="input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your question..."
              className="query-input"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !query.trim()} className="submit-btn">
              {loading ? 'Processing...' : 'Ask'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {response && (
          <div className="response-container">
            <div className="response-section">
              <h3>Answer</h3>
              <div className="answer-text">{response.answer}</div>
            </div>

            {response.transformed_query && response.transformed_query !== query && (
              <div className="response-section">
                <h4>Transformed Query</h4>
                <div className="transformed-query">{response.transformed_query}</div>
              </div>
            )}

            <div className="response-section">
              <h4>Sources ({response.chunks_retrieved})</h4>
              <div className="sources-list">
                {response.sources.map((source, idx) => (
                  <div key={idx} className="source-item">
                    <div className="source-name">{source.filename}</div>
                    <div className="source-meta">
                      <span>Technique: {source.technique}</span>
                      <span>Similarity: {(source.similarity * 100).toFixed(2)}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {response.tokens_used && (
              <div className="response-section">
                <h4>Token Usage</h4>
                <div className="token-info">
                  <span>Prompt: {response.tokens_used.prompt_tokens}</span>
                  <span>Completion: {response.tokens_used.completion_tokens}</span>
                  <span>Total: {response.tokens_used.total_tokens}</span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

