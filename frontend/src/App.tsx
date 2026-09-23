import React, { useState } from 'react';
import axios from 'axios';
import LoadingSpinner from './components/LoadingSpinner';
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
        setError('Network error or server unavailable');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Smart Guided Troubleshooter</h1>
      <p>Describe what's wrong with your device.</p>
      <input
        type="text"
        placeholder="My phone is getting very hot"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
        disabled={loading}
      />
      <button onClick={handleSubmit} disabled={loading || !query.trim()}>
        {loading ? 'Thinking…' : 'Troubleshoot'}
      </button>
      {loading && <LoadingSpinner />}
      {error && <div className="error">{error}</div>}
      {result && <ResultDisplay response={result} />}
    </div>
  );
}

export default App;
