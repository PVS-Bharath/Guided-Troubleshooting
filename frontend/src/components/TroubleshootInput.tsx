import React from 'react';

interface TroubleshootInputProps {
  query: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
}

interface SampleQuery {
  icon: string;
  label: string;
  text: string;
}

const SAMPLE_QUERIES: SampleQuery[] = [
  { icon: '🔥', label: 'Overheating', text: 'My phone is getting very hot' },
  { icon: '🔋', label: 'Battery', text: 'Battery drains unusually fast' },
  { icon: '📶', label: 'Wi-Fi', text: 'Wi-Fi disconnects frequently' },
  { icon: '⚡', label: 'Charging', text: 'Phone charges slowly or stops charging' },
  { icon: '📱', label: 'Screen', text: 'Screen flickers or dims unexpectedly' },
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
    <section className="input-section" aria-label="Device problem input">
      <div className="input-card">
        <div className="input-header-row">
          <div className="input-label-group">
            <span className="sparkle-accent">✨</span>
            <label htmlFor="device-issue-input" className="input-label">
              Describe your device issue
            </label>
          </div>
          <span className="input-hint">Natural language • AI-powered diagnosis</span>
        </div>
        
        <div className="input-field-wrapper">
          <div className="input-icon-wrapper">
            <svg
              className="input-search-icon"
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
          </div>

          <input
            id="device-issue-input"
            type="text"
            className="problem-input"
            placeholder="Type your complaint (e.g. My phone is getting very hot)..."
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
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          )}

          <button
            type="button"
            className={`submit-button ${loading ? 'is-loading' : ''}`}
            onClick={onSubmit}
            disabled={loading || !query.trim()}
          >
            {loading ? (
              <>
                <span className="button-spinner" aria-hidden="true"></span>
                <span>Diagnosing...</span>
              </>
            ) : (
              <>
                <span>Troubleshoot</span>
                <span className="kbd-shortcut" aria-hidden="true">↵</span>
              </>
            )}
          </button>
        </div>

        <div className="suggestion-pills-container">
          <div className="pills-header">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="lightbulb-icon">
              <path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-7 7c0 2.5 1.5 4.5 3 6h8c1.5-1.5 3-3.5 3-6a7 7 0 0 0-7-7z"></path>
            </svg>
            <span>Quick sample issues:</span>
          </div>

          <div className="suggestion-pills">
            {SAMPLE_QUERIES.map((sample) => (
              <button
                key={sample.label}
                type="button"
                className={`pill-button ${query === sample.text ? 'is-active' : ''}`}
                onClick={() => onChange(sample.text)}
                disabled={loading}
              >
                <span className="pill-icon">{sample.icon}</span>
                <span className="pill-text">{sample.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
