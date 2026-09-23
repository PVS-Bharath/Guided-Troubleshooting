// src/components/ResultDisplay.tsx
import React from 'react';
import type { TroubleshootResponse } from '../types';

interface Props {
  response: TroubleshootResponse;
}

export default function ResultDisplay({ response }: Props) {
  return (
    <div className="result">
      <h2>Problem</h2>
      <p>{response.query}</p>

      <h2>Goal</h2>
      <p>{response.goal}</p>

      <h2>Recommended Actions</h2>
      <ul>
        {response.actions.map((action, idx) => (
          <li key={idx} className="action-item">
            <strong>{action.actionName}</strong>
            <span className="mock-badge">mock</span>: {action.description}
            <ol>
              {action.steps.map((step, sIdx) => (
                <li key={sIdx}>{step}</li>
              ))}
            </ol>
            {action.deeplink && (
              <a href={action.deeplink} target="_blank" rel="noopener noreferrer">
                Open Settings (development mock – not an official Samsung deeplink)
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
