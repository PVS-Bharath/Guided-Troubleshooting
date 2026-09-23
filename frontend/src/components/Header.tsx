import React from 'react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="brand-badge">
        <span className="brand-dot"></span>
        <span>Samsung PRISM GenAI • Theme 02</span>
      </div>
      <h1 className="header-title">Smart Guided Troubleshooter</h1>
      <p className="header-subtitle">
        AI-driven diagnostic assistance and verified step-by-step resolution for Galaxy devices.
      </p>
    </header>
  );
}
