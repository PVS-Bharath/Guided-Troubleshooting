import React from 'react';
import type { TroubleshootResponse, ActionStep } from '../types';
import StepList from './StepList';

interface ResultDisplayProps {
  response: TroubleshootResponse;
}

export default function ResultDisplay({ response }: ResultDisplayProps) {
  return (
    <section className="result-container" aria-label="Troubleshooting results">
      {/* Overview diagnosis card */}
      <div className="diagnosis-card">
        <div className="card-top-bar">
          <div className="status-badge success">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="status-badge-icon">
              <path d="M20 6L9 17l-5-5"></path>
            </svg>
            <span>Diagnosis Complete</span>
          </div>
          {response.request_id && (
            <span className="trace-id" title={`Trace ID: ${response.request_id}`}>
              ID: {response.request_id.slice(0, 8)}...
            </span>
          )}
        </div>

        <div className="diagnosis-grid">
          <div className="diagnosis-item">
            <span className="diagnosis-label">Reported Issue</span>
            <p className="diagnosis-value query-text">"{response.query}"</p>
          </div>

          <div className="diagnosis-item">
            <span className="diagnosis-label">Target Resolution Goal</span>
            <div className="goal-pill">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="goal-icon">
                <circle cx="12" cy="12" r="10"></circle>
                <circle cx="12" cy="12" r="6"></circle>
                <circle cx="12" cy="12" r="2"></circle>
              </svg>
              <span>{response.goal}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommended actions header */}
      <div className="section-heading">
        <h2>Recommended Resolution</h2>
        <span className="heading-sub">Follow the recommended actions to resolve this device issue</span>
      </div>

      {/* Action cards */}
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
                  <div>
                    <div className="action-name-row">
                      <h3 className="action-name">{action.actionName}</h3>
                      {action.category && (
                        <span className="category-pill">{action.category}</span>
                      )}
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
                  <div className="deeplink-wrapper">
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
                      <span>Open Device Settings</span>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="external-icon">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" y1="14" x2="21" y2="3"></line>
                      </svg>
                    </a>

                    {isMock && (
                      <span className="dev-mock-tag" title="This is a development mock link, not an official Samsung deeplink">
                        DEV: mock deeplink ({action.deeplink})
                      </span>
                    )}
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
