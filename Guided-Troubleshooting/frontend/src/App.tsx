import React, { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import TroubleshootInput from './components/TroubleshootInput';
import LoadingState from './components/LoadingState';
import ErrorState from './components/ErrorState';
import EmptyState from './components/EmptyState';
import ResultDisplay from './components/ResultDisplay';
import type { TroubleshootResponse } from './types';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TroubleshootResponse | null>(null);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await axios.post<TroubleshootResponse>('/api/troubleshoot', { query });
      setResult(response.data);
    } catch (e: any) {
      if (e.response) {
        setError(`Error ${e.response.status}: ${e.response.data.detail || e.response.statusText}`);
      } else {
        setError('Network error or server unavailable. Please check backend connection.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setQuery('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="app-shell">
      <div className="app-container">
        <Header />

        <TroubleshootInput
          query={query}
          onChange={setQuery}
          onSubmit={handleSubmit}
          loading={loading}
        />

        <main className="content-area">
          {loading && <LoadingState />}

          {!loading && error && (
            <ErrorState message={error} onRetry={handleSubmit} />
          )}

          {!loading && !error && result && (
            <ResultDisplay response={result} onReset={handleReset} />
          )}

          {!loading && !error && !result && (
            <EmptyState onSelectSample={(sample) => setQuery(sample)} />
          )}
        </main>

        <footer className="app-footer">
          <div className="footer-content">
            <span className="footer-brand">SAMSUNG</span>
            <span className="footer-dot">•</span>
            <span>Samsung PRISM GenAI Hackathon 3rd Edition (2026–27)</span>
            <span className="footer-dot">•</span>
            <span>Theme 02: Smart Guided Troubleshooting Engine</span>
            <span className="footer-dot">•</span>
            <span>Team Srm_Devlopers</span>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
