import React from 'react';

export default function EmptyState() {
  return (
    <div className="empty-state-container">
      <div className="empty-icon-bubble">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.75"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="empty-icon"
        >
          <rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect>
          <line x1="12" y1="18" x2="12.01" y2="18"></line>
          <path d="M9 7h6"></path>
          <path d="M9 11h6"></path>
        </svg>
      </div>
      <h3 className="empty-title">How can we assist with your Galaxy device?</h3>
      <p className="empty-description">
        Type any symptom or question above. The Smart Guided Troubleshooter will diagnose the issue,
        identify the targeted goal, and provide direct, step-by-step instructions.
      </p>

      <div className="empty-features-grid">
        <div className="feature-item">
          <div className="feature-icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
            </svg>
          </div>
          <div>
            <div className="feature-title">AI Intent Diagnosis</div>
            <div className="feature-desc">Interprets natural complaints into specific device goals</div>
          </div>
        </div>

        <div className="feature-item">
          <div className="feature-icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
          </div>
          <div>
            <div className="feature-title">Ordered UI Steps</div>
            <div className="feature-desc">Actionable navigation paths matching Samsung device screens</div>
          </div>
        </div>

        <div className="feature-item">
          <div className="feature-icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <div>
            <div className="feature-title">Settings Deeplinks</div>
            <div className="feature-desc">Direct shortcuts into the relevant Samsung settings menu</div>
          </div>
        </div>
      </div>
    </div>
  );
}
