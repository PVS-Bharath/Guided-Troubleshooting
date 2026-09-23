import React, { useState } from 'react';

interface StepListProps {
  steps: string[];
}

export default function StepList({ steps }: StepListProps) {
  const [completedSteps, setCompletedSteps] = useState<Record<number, boolean>>({});

  if (!steps || steps.length === 0) {
    return null;
  }

  const toggleStep = (index: number) => {
    setCompletedSteps((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const completedCount = steps.filter((_, idx) => !!completedSteps[idx]).length;
  const progressPercent = Math.round((completedCount / steps.length) * 100);
  const allCompleted = completedCount === steps.length && steps.length > 0;

  return (
    <div className="stepper-container" aria-label="Guided troubleshooting steps">
      <div className="stepper-header-bar">
        <div className="stepper-title-group">
          <span className="stepper-title">Guided Action Steps</span>
          <span className="stepper-subtext">Click any step as you complete it on your device</span>
        </div>

        <div className="progress-badge">
          <span className="progress-counter">
            {completedCount} of {steps.length} done
          </span>
          <span className="progress-pill">{progressPercent}%</span>
        </div>
      </div>

      {/* Interactive Progress Bar */}
      <div className="step-progress-track">
        <div
          className={`step-progress-fill ${allCompleted ? 'is-complete' : ''}`}
          style={{ width: `${progressPercent}%` }}
        ></div>
      </div>

      {allCompleted && (
        <div className="all-steps-completed-banner" role="status">
          <span className="check-all-icon">🎉</span>
          <div>
            <strong>All troubleshooting steps marked complete!</strong>
            <p>Check if the device symptom has resolved or restart your device.</p>
          </div>
        </div>
      )}

      <ol className="stepper-list">
        {steps.map((step, index) => {
          const stepNumber = index + 1;
          const isDone = !!completedSteps[index];
          const isLast = index === steps.length - 1;

          return (
            <li
              key={index}
              className={`stepper-item ${isDone ? 'is-completed' : ''} ${isLast ? 'is-last' : ''}`}
            >
              <button
                type="button"
                className="stepper-node-button"
                onClick={() => toggleStep(index)}
                aria-label={`Toggle step ${stepNumber}: ${step}`}
                title="Click to mark as done"
              >
                <div className={`stepper-badge ${isDone ? 'done' : ''}`}>
                  {isDone ? (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="check-svg">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  ) : (
                    <span>{stepNumber}</span>
                  )}
                </div>
                {!isLast && <span className={`stepper-line ${isDone ? 'active' : ''}`} aria-hidden="true"></span>}
              </button>

              <div
                className={`stepper-content-card ${isDone ? 'done-card' : ''}`}
                onClick={() => toggleStep(index)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleStep(index);
                  }
                }}
              >
                <div className="step-card-header">
                  <span className="step-tag">Step {stepNumber}</span>
                  <span className="step-status-hint">
                    {isDone ? '✓ Completed' : 'Click to complete'}
                  </span>
                </div>
                <p className="stepper-instruction">{step}</p>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
