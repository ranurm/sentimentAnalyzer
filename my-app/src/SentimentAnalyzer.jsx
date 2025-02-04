import React, { useState } from 'react';
import './SentimentAnalyzer.css';

function SentimentAnalyzer() {
  const [text, setText] = useState('');
  const [model, setModel] = useState('custom');
  const [sentiment, setSentiment] = useState('');
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, model }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSentiment(data.sentiment);
      setConfidence(data.confidence);
    } catch (err) {
      console.error("Error during analysis:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Sentiment Analysis</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text for analysis..."
        rows={8}
        className="text-area"
      />

      <div className="input-group">
        <select value={model} onChange={(e) => setModel(e.target.value)} className="model-select">
          <option value="custom">Custom Model</option>
          <option value="llama">Llama 3</option>
        </select>

        <button onClick={handleAnalyze} disabled={loading} className="analyze-button">
          {loading ? "Analyzing..." : "Analyze Sentiment"}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {sentiment && (
        <div className="result">
          <h2>Result:</h2>
          <p className={`sentiment ${sentiment}`}>Sentiment: {sentiment}</p>
          {confidence !== null && <p>Confidence: {confidence.toFixed(2)}</p>}
        </div>
      )}
    </div>
  );
}

export default SentimentAnalyzer;