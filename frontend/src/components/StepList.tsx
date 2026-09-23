import React from 'react';

interface StepListProps {
  steps: string[];
}

export default function StepList({ steps }: StepListProps) {
  if (!steps || steps.length === 0) {
    return null;
  }

  return (
    <div className="stepper-container">
      <div className="stepper-header">
        <span className="stepper-title">Step-by-step resolution:</span>
        <span className="stepper-count">{steps.length} {steps.length === 1 ? 'step' : 'steps'}</span>
      </div>

      <ol className="stepper-list">
        {steps.map((step, index) => {
          const stepNumber = index + 1;
          const isLast = index === steps.length - 1;

          return (
            <li key={index} className={`stepper-item ${isLast ? 'is-last' : ''}`}>
              <div className="stepper-node">
                <span className="stepper-badge">{stepNumber}</span>
                {!isLast && <span className="stepper-line" aria-hidden="true"></span>}
              </div>

              <div className="stepper-content-card">
                <div className="stepper-step-number">Step {stepNumber}</div>
                <div className="stepper-instruction">{step}</div>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
