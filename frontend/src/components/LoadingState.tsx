import React, { useState, useEffect } from 'react';

const DIAGNOSTIC_STAGES = [
  'Processing natural language complaint...',
  'Interpreting device symptoms & root causes...',
  'Retrieving verified resolution knowledge base...',
  'Mapping official Samsung Settings deeplinks...',
];

export default function LoadingState() {
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStage((prev) => (prev + 1) % DIAGNOSTIC_STAGES.length);
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-state-container" aria-live="polite">
      {/* Galaxy AI Orbital Scanner */}
      <div className="galaxy-orbital-scanner">
        <div className="orbital-ring outer"></div>
        <div className="orbital-ring inner"></div>
        <div className="orbital-core">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="core-icon">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
          </svg>
        </div>
      </div>

      <div className="loading-status-group">
        <div className="loading-pill-badge">
          <span className="live-sparkle">✦</span>
          <span>Galaxy AI Diagnostics</span>
        </div>
        <h3 className="loading-title">Analyzing your device issue...</h3>
        <p className="loading-stage-text">{DIAGNOSTIC_STAGES[currentStage]}</p>
      </div>

      {/* Interactive Progress Track */}
      <div className="diagnostic-progress-track">
        <div className="progress-bar-fill animated"></div>
      </div>

      {/* Shimmering Skeleton Result Preview */}
      <div className="skeleton-card">
        <div className="skeleton-card-top">
          <div className="skeleton-badge shimmer"></div>
          <div className="skeleton-id shimmer"></div>
        </div>

        <div className="skeleton-grid">
          <div className="skeleton-col">
            <div className="skeleton-label shimmer"></div>
            <div className="skeleton-box shimmer"></div>
          </div>
          <div className="skeleton-col">
            <div className="skeleton-label shimmer"></div>
            <div className="skeleton-box shimmer"></div>
          </div>
        </div>

        <div className="skeleton-steps-block">
          <div className="skeleton-step-row">
            <div className="skeleton-circle shimmer"></div>
            <div className="skeleton-line shimmer full"></div>
          </div>
          <div className="skeleton-step-row">
            <div className="skeleton-circle shimmer"></div>
            <div className="skeleton-line shimmer three-quarter"></div>
          </div>
          <div className="skeleton-step-row">
            <div className="skeleton-circle shimmer"></div>
            <div className="skeleton-line shimmer half"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
