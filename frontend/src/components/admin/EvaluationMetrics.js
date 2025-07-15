import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function EvaluationMetrics() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/evaluate')
      .then(res => {
        setMetrics(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading evaluation metrics...</div>;
  if (!metrics) return <div>Could not load metrics.</div>;

  return (
    <div style={{
      border: '1px solid #eee', borderRadius: 8, padding: 24, margin: 24, background: '#fafbfc'
    }}>
      <h2>Evaluation Metrics</h2>
      <ul>
        <li><strong>Precision@K:</strong> {metrics['precision@k']}</li>
        <li><strong>Recall@K:</strong> {metrics['recall@k']}</li>
        <li><strong>F1@K:</strong> {metrics['f1@k']}</li>
        <li><strong>NDCG@K:</strong> {metrics['ndcg@k']}</li>
      </ul>
    </div>
  );
} 