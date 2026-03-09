import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import { getJobs } from '../services/jobService';
import { getResumes } from '../services/resumeService';
import { calculateMatches } from '../services/matchService';
import MatchCalculation from '../components/matches/MatchCalculation';
import MatchResults from '../components/matches/MatchResults';
import MatchVisualization from '../components/matches/MatchVisualization';

const PageContainer = styled.div`
  padding-top: 80px;
  min-height: 100vh;
  background-color: ${props => props.theme.colors.background};
`;

const ContentContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: ${props => props.theme.spacing.xl};
`;

const PageTitle = styled.h1`
  margin-bottom: ${props => props.theme.spacing.lg};
  color: ${props => props.theme.colors.text};
`;

const SectionTitle = styled.h2`
  font-size: ${props => props.theme.fontSizes.large};
  margin-top: ${props => props.theme.spacing.xl};
  margin-bottom: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.text};
`;

const FilterBar = styled.div`
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
`;

const FilterLabel = styled.label`
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: #495057;
  font-weight: 500;
`;

const FilterInput = styled.input`
  padding: 6px 10px;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  font-size: 0.9rem;
  width: 80px;
`;

const FilterSelect = styled.select`
  padding: 6px 10px;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  font-size: 0.9rem;
`;

const Loader = styled.div`
  text-align: center;
  padding: 48px 0;
  color: #6c757d;
  font-size: 1.1rem;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 48px 0;
  color: #6c757d;
`;

const SummaryBar = styled.div`
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  flex-wrap: wrap;
`;

const SummaryItem = styled.div`
  background: #fff;
  border-radius: 10px;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  text-align: center;
  flex: 1;
  min-width: 120px;
`;

const SummaryValue = styled.div`
  font-size: 1.75rem;
  font-weight: 700;
  color: ${props => props.color || '#4361ee'};
`;

const SummaryLabel = styled.div`
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 4px;
`;

const MatchesPage = () => {
  const [jobs, setJobs] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState('');
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [minScore, setMinScore] = useState(0);
  const [sortBy, setSortBy] = useState('score');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [jobsData, resumesData] = await Promise.all([getJobs(), getResumes()]);
        setJobs(jobsData);
        setResumes(resumesData);
        if (jobsData.length > 0) {
          setSelectedJobId(jobsData[0].id);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const handleCalculateMatches = async () => {
    if (!selectedJobId) return;
    setLoading(true);
    try {
      const matchResults = await calculateMatches(selectedJobId);
      setMatches(matchResults);
    } catch (error) {
      console.error('Error calculating matches:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredMatches = matches
    .filter(m => m.score * 100 >= minScore)
    .sort((a, b) => sortBy === 'score' ? b.score - a.score : 0);

  const avgScore = matches.length > 0
    ? Math.round(matches.reduce((sum, m) => sum + m.score, 0) / matches.length * 100)
    : 0;

  const highCount = matches.filter(m => m.score >= 0.7).length;

  return (
    <>
      <Header />
      <PageContainer>
        <ContentContainer>
          <PageTitle>Match Results</PageTitle>

          <MatchCalculation
            jobs={jobs}
            selectedJobId={selectedJobId}
            onJobChange={setSelectedJobId}
            onCalculate={handleCalculateMatches}
            loading={loading}
          />

          {loading ? (
            <Loader>Calculating matches...</Loader>
          ) : matches.length > 0 ? (
            <>
              <SummaryBar>
                <SummaryItem>
                  <SummaryValue>{matches.length}</SummaryValue>
                  <SummaryLabel>Total Matches</SummaryLabel>
                </SummaryItem>
                <SummaryItem>
                  <SummaryValue color="#4bb543">{avgScore}%</SummaryValue>
                  <SummaryLabel>Average Score</SummaryLabel>
                </SummaryItem>
                <SummaryItem>
                  <SummaryValue color="#4361ee">{highCount}</SummaryValue>
                  <SummaryLabel>High Matches (70%+)</SummaryLabel>
                </SummaryItem>
                <SummaryItem>
                  <SummaryValue color="#ffc107">
                    {Math.round(Math.max(...matches.map(m => m.score)) * 100)}%
                  </SummaryValue>
                  <SummaryLabel>Best Score</SummaryLabel>
                </SummaryItem>
              </SummaryBar>

              <SectionTitle>Visualizations</SectionTitle>
              <MatchVisualization matches={matches} resumes={resumes} />

              <SectionTitle>Candidate Results</SectionTitle>
              <FilterBar>
                <FilterLabel>
                  Min Score:
                  <FilterInput
                    type="number"
                    value={minScore}
                    onChange={e => setMinScore(Number(e.target.value))}
                    min={0}
                    max={100}
                  />
                </FilterLabel>
                <FilterLabel>
                  Sort By:
                  <FilterSelect value={sortBy} onChange={e => setSortBy(e.target.value)}>
                    <option value="score">Score (High to Low)</option>
                  </FilterSelect>
                </FilterLabel>
              </FilterBar>

              <MatchResults matches={filteredMatches} resumes={resumes} />
            </>
          ) : selectedJobId && !loading ? (
            <EmptyState>
              <p>No matches found. Try selecting a different job or upload more resumes.</p>
            </EmptyState>
          ) : null}
        </ContentContainer>
      </PageContainer>
      <Footer />
    </>
  );
};

export default MatchesPage;
