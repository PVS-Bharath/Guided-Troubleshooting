import React from 'react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-meta-row">
        <div className="brand-badge">
          <span className="brand-sparkle">✦</span>
          <span>Samsung PRISM GenAI • Theme 02</span>
        </div>
        <div className="device-status-pill">
          <span className="status-live-dot"></span>
          <span>Galaxy Diagnostics • Online</span>
        </div>
      </div>

      <div className="header-brand-hero">
        <div className="samsung-logo-tag">SAMSUNG</div>
        <h1 className="header-title">Smart Guided Troubleshooter</h1>
        <p className="header-subtitle">
          Intelligent device diagnostics, root-cause goal interpretation, and verified 
          step-by-step resolution pathways for your Galaxy device.
        </p>
      </div>
    </header>
  );
}
