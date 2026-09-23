import React from 'react';

interface TroubleshootInputProps {
  query: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
}

const SAMPLE_QUERIES = [
  'My phone is getting very hot',
  'Battery drains unusually fast',
  'Wi-Fi disconnects frequently',
  'Screen flickers when charging',
];

export default function TroubleshootInput({
  query,
  onChange,
  onSubmit,
  loading,
}: TroubleshootInputProps) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !loading && query.trim()) {
      onSubmit();
    }
  };

  return (
    <section className="input-section">
      <div className="input-card">
        <label htmlFor="device-issue-input" className="input-label">
          Describe what's wrong with your device
        </label>
        
        <div className="input-field-wrapper">
          <svg
            className="input-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>

          <input
            id="device-issue-input"
            type="text"
            className="problem-input"
            placeholder="Describe the issue (e.g., My phone is getting very hot)..."
            value={query}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            autoComplete="off"
          />

          {query && !loading && (
            <button
              type="button"
              className="clear-button"
              onClick={() => onChange('')}
              title="Clear input"
              aria-label="Clear input"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          )}

          <button
            type="button"
            className="submit-button"
            onClick={onSubmit}
            disabled={loading || !query.trim()}
          >
            {loading ? (
              <>
                <span className="button-spinner" aria-hidden="true"></span>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <span>Troubleshoot</span>
                <svg
                  className="button-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </>
            )}
          </button>
        </div>

        <div className="suggestion-pills">
          <span className="pills-label">Common issues:</span>
          {SAMPLE_QUERIES.map((sample) => (
            <button
              key={sample}
              type="button"
              className="pill-button"
              onClick={() => onChange(sample)}
              disabled={loading}
            >
              {sample}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
