import React from 'react';

export default function LoadingState() {
  return (
    <div className="loading-state-container" aria-live="polite">
      <div className="diagnostic-pulse-badge">
        <div className="pulse-ring"></div>
        <div className="pulse-core">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
          </svg>
        </div>
      </div>

      <h3 className="loading-title">Analyzing your issue...</h3>
      <p className="loading-subtitle">
        Evaluating device symptoms, retrieving verified knowledge, and mapping resolution steps.
      </p>

      {/* Skeleton card preview to avoid layout shifts */}
      <div className="skeleton-card">
        <div className="skeleton-line skeleton-title"></div>
        <div className="skeleton-line skeleton-text"></div>
        <div className="skeleton-steps">
          <div className="skeleton-step-item">
            <div className="skeleton-circle"></div>
            <div className="skeleton-line skeleton-step-line"></div>
          </div>
          <div className="skeleton-step-item">
            <div className="skeleton-circle"></div>
            <div className="skeleton-line skeleton-step-line short"></div>
          </div>
          <div className="skeleton-step-item">
            <div className="skeleton-circle"></div>
            <div className="skeleton-line skeleton-step-line medium"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
