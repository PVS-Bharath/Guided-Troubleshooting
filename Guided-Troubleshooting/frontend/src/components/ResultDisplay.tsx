import React, { useState } from 'react';
import type { TroubleshootResponse, ActionStep } from '../types';
import StepList from './StepList';

interface ResultDisplayProps {
  response: TroubleshootResponse;
  onReset?: () => void;
}

export default function ResultDisplay({ response, onReset }: ResultDisplayProps) {
  const [copiedId, setCopiedId] = useState(false);

  const handleCopyId = () => {
    if (!response.request_id) return;
    navigator.clipboard.writeText(response.request_id);
    setCopiedId(true);
    setTimeout(() => setCopiedId(false), 2000);
  };

  return (
    <section className="result-container" aria-label="Troubleshooting results">
      {/* Overview diagnosis card */}
      <div className="diagnosis-card">
        <div className="card-top-bar">
          <div className="status-badge success">
            <span className="badge-sparkle">✦</span>
            <span>Diagnosis Verified</span>
          </div>

          {response.request_id && (
            <div className="trace-id-group">
              <span className="trace-id-label">Trace:</span>
              <button
                type="button"
                className="trace-id-pill"
                onClick={handleCopyId}
                title="Click to copy full request ID"
              >
                <span>{response.request_id.slice(0, 8)}...</span>
                <span className="copy-icon-label">{copiedId ? '✓' : '⧉'}</span>
              </button>
            </div>
          )}
        </div>

        <div className="diagnosis-grid">
          <div className="diagnosis-item issue-item">
            <span className="diagnosis-label">Reported Device Symptom</span>
            <p className="diagnosis-value query-text">"{response.query}"</p>
          </div>

          <div className="diagnosis-item goal-item">
            <span className="diagnosis-label">Target Resolution Goal</span>
            <div className="goal-pill">
              <span className="goal-sparkle">🎯</span>
              <span className="goal-text">{response.goal}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Section Heading with action count */}
      <div className="section-heading-bar">
        <div>
          <h2 className="section-heading-title">Recommended Resolution</h2>
          <p className="section-heading-sub">
            Follow the guided actions below in sequence to resolve your device problem
          </p>
        </div>

        {onReset && (
          <button type="button" className="new-search-btn" onClick={onReset}>
            <span>+ Troubleshoot Another Issue</span>
          </button>
        )}
      </div>

      {/* Action cards list */}
      <div className="action-cards-list">
        {response.actions.map((action: ActionStep, idx: number) => {
          const isMock = action.is_mock !== false;

          return (
            <article key={idx} className="action-card">
              <div className="action-card-header">
                <div className="action-title-group">
                  <div className="action-icon-circle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                      <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                    </svg>
                  </div>
                  <div className="action-header-details">
                    <div className="action-name-row">
                      <h3 className="action-name">{action.actionName}</h3>
                      {action.category && (
                        <span className="category-pill">{action.category}</span>
                      )}
                      <span className="primary-pill">Recommended</span>
                    </div>
                    <p className="action-description">{action.description}</p>
                  </div>
                </div>
              </div>

              {/* Stepper with ordered steps */}
              <div className="action-card-body">
                <StepList steps={action.steps} />
              </div>

              {/* Deeplink & Action Footer */}
              {action.deeplink && (
                <div className="action-card-footer">
                  <div className="deeplink-container">
                    <div className="deeplink-btn-group">
                      <a
                        href={action.deeplink}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="deeplink-button"
                        title={action.deeplink}
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="settings-icon">
                          <circle cx="12" cy="12" r="3"></circle>
                          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                        </svg>
                        <span>Open Settings Shortcut</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="external-arrow-icon">
                          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                          <polyline points="15 3 21 3 21 9"></polyline>
                          <line x1="10" y1="14" x2="21" y2="3"></line>
                        </svg>
                      </a>

                      {isMock && (
                        <span className="dev-mock-badge" title="Development placeholder mock link">
                          ⚙️ DEV: mock deeplink ({action.deeplink})
                        </span>
                      )}
                    </div>

                    <span className="deeplink-helper-note">
                      Jumps directly to the relevant Samsung Galaxy device settings screen
                    </span>
                  </div>
                </div>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
