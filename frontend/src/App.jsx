import React, { useState } from 'react';
import InputForm from './components/InputForm';
import AgentStatus from './components/AgentStatus';
import ResultCard from './components/ResultCard';

const App = () => {
  const [status, setStatus] = useState('idle'); // idle, generating, reviewing, complete
  const [result, setResult] = useState(null);

  const handleGenerate = async ({ grade, topic }) => {
    setStatus('generating');
    setResult(null);

    // Simulate steps for visual effect before actual call finishes (since the backend does it all in one go for now)
    // In a real socket/streamed app, we'd get real updates. We'll fake the "agent handoff" visually.

    const API_URL = import.meta.env.VITE_API_BASE_URL || (window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : '');

    try {
      const response = await fetch(`${API_URL}/api/generate-content`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grade, topic }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Generation failed');
      }

      const data = await response.json();

      // Artificial delay to show "Reviewer" working
      setStatus('reviewing');
      setTimeout(() => {
        setResult(data);
        setStatus('complete');
      }, 1500);

    } catch (e) {
      console.error(e);
      setStatus('idle');
      alert(`Error: ${e.message}`);
    }
  };

  return (
    <div className="container">
      <header style={{ marginBottom: '3rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>
          <span style={{ color: '#6366f1' }}>Smart</span>Edu Agents
        </h1>
        <p style={{ color: 'var(--text-muted)' }}>AI-Powered Educational Content Pipeline</p>
      </header>

      <InputForm onSubmit={handleGenerate} isLoading={status !== 'idle' && status !== 'complete'} />

      {status !== 'idle' && (
        <AgentStatus step={status} status={result?.final_status} />
      )}

      {status === 'complete' && result && (
        <ResultCard data={result} />
      )}
    </div>
  );
};

export default App;
