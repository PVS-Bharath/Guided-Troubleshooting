import React from 'react';

interface EmptyStateProps {
  onSelectSample?: (query: string) => void;
}

interface DiagnosticCategory {
  icon: string;
  title: string;
  subtitle: string;
  sampleQuery: string;
}

const CATEGORIES: DiagnosticCategory[] = [
  {
    icon: '🔥',
    title: 'Temperature & Heat',
    subtitle: 'Overheating during usage or charging',
    sampleQuery: 'My phone is getting very hot',
  },
  {
    icon: '🔋',
    title: 'Battery & Power',
    subtitle: 'Abnormal drain or slow charging cycles',
    sampleQuery: 'Battery drains unusually fast',
  },
  {
    icon: '📶',
    title: 'Connectivity',
    subtitle: 'Wi-Fi drops, Bluetooth, or mobile network',
    sampleQuery: 'Wi-Fi disconnects frequently',
  },
  {
    icon: '📱',
    title: 'Display & Touch',
    subtitle: 'Flickering, auto-dimming, or unresponsive touch',
    sampleQuery: 'Screen flickers or dims unexpectedly',
  },
];

export default function EmptyState({ onSelectSample }: EmptyStateProps) {
  return (
    <div className="empty-state-container" aria-label="Device diagnostic welcome">
      <div className="empty-hero-section">
        <div className="empty-icon-shield">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" className="shield-svg">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            <path d="M9 12l2 2 4-4"></path>
          </svg>
        </div>
        <h3 className="empty-title">How can we assist with your Galaxy device?</h3>
        <p className="empty-description">
          Describe any symptom in your own words above, or choose a common diagnostic category below to start 
          guided troubleshooting with verified Samsung Settings navigation steps.
        </p>
      </div>

      <div className="category-cards-grid">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.title}
            type="button"
            className="category-card"
            onClick={() => onSelectSample && onSelectSample(cat.sampleQuery)}
          >
            <div className="category-icon-box">{cat.icon}</div>
            <div className="category-text">
              <span className="category-name">{cat.title}</span>
              <span className="category-desc">{cat.subtitle}</span>
            </div>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="category-arrow">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        ))}
      </div>

      <div className="trust-footer-strip">
        <div className="trust-badge">
          <span className="trust-icon">✓</span>
          <span>Verified UI Navigation Steps</span>
        </div>
        <div className="trust-badge">
          <span className="trust-icon">⚡</span>
          <span>Official Samsung Settings Shortcuts</span>
        </div>
        <div className="trust-badge">
          <span className="trust-icon">🔒</span>
          <span>Local Device Privacy Protected</span>
        </div>
      </div>
    </div>
  );
}
