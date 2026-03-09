import React from 'react';
import styled from 'styled-components';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Bar, Doughnut, Radar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
);

const VisualizationContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-top: 24px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ChartCard = styled.div`
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
`;

const ChartTitle = styled.h3`
  font-size: 1rem;
  color: #212529;
  margin-bottom: 16px;
  font-weight: 600;
`;

const MatchVisualization = ({ matches = [], resumes = [] }) => {
  if (!matches || matches.length === 0) {
    return null;
  }

  // Score Distribution Bar Chart
  const scoreLabels = matches.slice(0, 10).map((m, i) => {
    const resume = resumes.find(r => r.id === m.resume_id);
    return resume?.name || `Candidate ${i + 1}`;
  });
  const scoreValues = matches.slice(0, 10).map(m => Math.round(m.score * 100));

  const barData = {
    labels: scoreLabels,
    datasets: [
      {
        label: 'Match Score (%)',
        data: scoreValues,
        backgroundColor: scoreValues.map(v =>
          v >= 70 ? 'rgba(75, 181, 67, 0.7)' :
          v >= 40 ? 'rgba(255, 193, 7, 0.7)' :
          'rgba(255, 51, 51, 0.7)'
        ),
        borderColor: scoreValues.map(v =>
          v >= 70 ? 'rgb(75, 181, 67)' :
          v >= 40 ? 'rgb(255, 193, 7)' :
          'rgb(255, 51, 51)'
        ),
        borderWidth: 2,
        borderRadius: 6,
      }
    ]
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: false },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: { callback: val => val + '%' }
      },
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 0,
          font: { size: 11 }
        }
      }
    }
  };

  // Score Distribution Doughnut
  const highMatches = matches.filter(m => m.score >= 0.7).length;
  const mediumMatches = matches.filter(m => m.score >= 0.4 && m.score < 0.7).length;
  const lowMatches = matches.filter(m => m.score < 0.4).length;

  const doughnutData = {
    labels: ['High (70%+)', 'Medium (40-70%)', 'Low (<40%)'],
    datasets: [
      {
        data: [highMatches, mediumMatches, lowMatches],
        backgroundColor: [
          'rgba(75, 181, 67, 0.8)',
          'rgba(255, 193, 7, 0.8)',
          'rgba(255, 51, 51, 0.8)'
        ],
        borderColor: ['rgb(75, 181, 67)', 'rgb(255, 193, 7)', 'rgb(255, 51, 51)'],
        borderWidth: 2,
      }
    ]
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { position: 'bottom' }
    }
  };

  // Skills Radar Chart - aggregate skills across top matches
  const allMatchingSkills = {};
  const allMissingSkills = {};
  matches.slice(0, 5).forEach(m => {
    (m.details?.matching_skills || []).forEach(s => {
      allMatchingSkills[s] = (allMatchingSkills[s] || 0) + 1;
    });
    (m.details?.missing_skills || []).forEach(s => {
      allMissingSkills[s] = (allMissingSkills[s] || 0) + 1;
    });
  });

  const topSkills = Object.keys(allMatchingSkills)
    .sort((a, b) => allMatchingSkills[b] - allMatchingSkills[a])
    .slice(0, 8);

  const radarData = topSkills.length > 2 ? {
    labels: topSkills,
    datasets: [
      {
        label: 'Skill Match Frequency',
        data: topSkills.map(s => allMatchingSkills[s] || 0),
        backgroundColor: 'rgba(67, 97, 238, 0.2)',
        borderColor: 'rgb(67, 97, 238)',
        borderWidth: 2,
        pointBackgroundColor: 'rgb(67, 97, 238)',
      }
    ]
  } : null;

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      r: {
        beginAtZero: true,
        ticks: { stepSize: 1 }
      }
    },
    plugins: {
      legend: { position: 'bottom' }
    }
  };

  // Score Trend (sorted scores)
  const sortedScores = [...matches].sort((a, b) => b.score - a.score).map(m => Math.round(m.score * 100));
  const trendLabels = sortedScores.map((_, i) => `#${i + 1}`);

  const trendData = {
    labels: trendLabels.slice(0, 15),
    datasets: [
      {
        label: 'Match Score (%)',
        data: sortedScores.slice(0, 15),
        backgroundColor: 'rgba(67, 97, 238, 0.1)',
        borderColor: 'rgb(67, 97, 238)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointBackgroundColor: 'rgb(67, 97, 238)',
      }
    ]
  };

  return (
    <VisualizationContainer>
      <ChartCard>
        <ChartTitle>Top Candidate Scores</ChartTitle>
        <Bar data={barData} options={barOptions} />
      </ChartCard>

      <ChartCard>
        <ChartTitle>Score Distribution</ChartTitle>
        <Doughnut data={doughnutData} options={doughnutOptions} />
      </ChartCard>

      {radarData && (
        <ChartCard>
          <ChartTitle>Top Matching Skills</ChartTitle>
          <Radar data={radarData} options={radarOptions} />
        </ChartCard>
      )}

      <ChartCard>
        <ChartTitle>Score Ranking (All Candidates)</ChartTitle>
        <Bar data={trendData} options={{
          ...barOptions,
          plugins: { legend: { display: true, position: 'bottom' } }
        }} />
      </ChartCard>
    </VisualizationContainer>
  );
};

export default MatchVisualization;
