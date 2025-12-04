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
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [activeTab, setActiveTab] = useState('query');

  useEffect(() => {
    fetchStats();
    fetchDocuments();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/stats`);
      setStats(res.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const fetchDocuments = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/documents`);
      setDocuments(res.data.documents || []);
    } catch (err) {
      console.error('Error fetching documents:', err);
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
      fetchDocuments();
      alert('Vector store rebuilt successfully');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to rebuild');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf') && !file.name.endsWith('.txt')) {
      setUploadError('Only PDF and TXT files are allowed');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      setUploadError('File size must be less than 50MB');
      return;
    }

    setUploading(true);
    setUploadError(null);
    setUploadSuccess(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setUploadSuccess(`File "${file.name}" uploaded successfully! ${res.data.chunks_created} chunks created.`);
      fetchStats();
      fetchDocuments();
      event.target.value = '';
    } catch (err) {
      setUploadError(err.response?.data?.error || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (filename) => {
    if (!window.confirm(`Delete document "${filename}"?`)) return;

    try {
      await axios.delete(`${API_BASE_URL}/api/documents/${filename}`);
      fetchDocuments();
      fetchStats();
      alert('Document deleted successfully');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete document');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>RAG-Powered Assistant</h1>
        <p>Upload documents, generate embeddings, and query using RAG</p>
      </header>

      <div className="container">
        <div className="tabs">
          <button 
            className={activeTab === 'upload' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('upload')}
          >
            Upload Documents
          </button>
          <button 
            className={activeTab === 'query' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('query')}
          >
            Query Documents
          </button>
        </div>

        {activeTab === 'upload' && (
          <div className="upload-section">
            <div className="upload-panel">
              <h3>Upload PDF or TXT Files</h3>
              <p>Upload 3-5 documents to build your knowledge base</p>
              
              <div className="upload-area">
                <input
                  type="file"
                  id="file-upload"
                  accept=".pdf,.txt"
                  onChange={handleFileUpload}
                  disabled={uploading}
                  style={{ display: 'none' }}
                />
                <label htmlFor="file-upload" className="upload-label">
                  {uploading ? 'Processing...' : 'Choose File (PDF or TXT)'}
                </label>
              </div>

              {uploadError && (
                <div className="error-message">{uploadError}</div>
              )}

              {uploadSuccess && (
                <div className="success-message">{uploadSuccess}</div>
              )}

              <div className="documents-list">
                <h4>Uploaded Documents ({documents.length})</h4>
                {documents.length === 0 ? (
                  <p className="no-docs">No documents uploaded yet</p>
                ) : (
                  <div className="documents-grid">
                    {documents.map((doc, idx) => (
                      <div key={idx} className="document-item">
                        <div className="doc-info">
                          <span className="doc-name">{doc.filename}</span>
                          <span className="doc-size">{(doc.size / 1024).toFixed(2)} KB</span>
                        </div>
                        <button
                          className="delete-btn"
                          onClick={() => handleDeleteDocument(doc.filename)}
                        >
                          Delete
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'query' && (
          <>
            <div className="stats-panel">
              {stats && (
                <div className="stats">
                  <span>Chunks: {stats.total_chunks}</span>
                  <span>Dimension: {stats.dimension}</span>
                  <span>Documents: {documents.length}</span>
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
          </>
        )}
      </div>
    </div>
  );
}

export default App;

