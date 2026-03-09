import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const ResultsContainer = styled.div`
  margin-top: 24px;
`;

const ResultCard = styled(motion.div)`
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 20px;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
  }
`;

const ScoreBadge = styled.div`
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: ${props =>
    props.score >= 70
      ? 'linear-gradient(135deg, #4bb543, #36a336)'
      : props.score >= 40
      ? 'linear-gradient(135deg, #ffc107, #e6a800)'
      : 'linear-gradient(135deg, #ff3333, #cc0000)'};
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.25rem;
  font-weight: 700;
  flex-shrink: 0;
`;

const Info = styled.div`
  flex: 1;
`;

const CandidateName = styled.h3`
  font-size: 1.1rem;
  margin-bottom: 4px;
  color: #212529;
`;

const Detail = styled.p`
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 8px;
`;

const SkillsRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
`;

const SkillChip = styled.span`
  font-size: 0.75rem;
  padding: 2px 10px;
  border-radius: 12px;
  background: ${props => props.matched ? 'rgba(75,181,67,0.12)' : 'rgba(255,51,51,0.1)'};
  color: ${props => props.matched ? '#2d8a2d' : '#cc0000'};
  font-weight: 500;
`;

const MatchResults = ({ matches = [], resumes = [] }) => {
  if (!matches || matches.length === 0) {
    return null;
  }

  return (
    <ResultsContainer>
      {matches.map((match, index) => {
        const resume = resumes.find(r => r.id === match.resume_id) || {};
        const score = Math.round(match.score * 100);

        return (
          <ResultCard
            key={match.id || index}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
          >
            <ScoreBadge score={score}>{score}%</ScoreBadge>
            <Info>
              <CandidateName>{resume.name || 'Unknown Candidate'}</CandidateName>
              <Detail>
                {resume.email || 'No email'} &bull; {resume.skills?.length || 0} skills &bull; {resume.experience?.length || 0} experience entries
              </Detail>
              <SkillsRow>
                {(match.details?.matching_skills || []).slice(0, 5).map((skill, i) => (
                  <SkillChip key={`m-${i}`} matched>{skill}</SkillChip>
                ))}
                {(match.details?.missing_skills || []).slice(0, 3).map((skill, i) => (
                  <SkillChip key={`x-${i}`}>{skill}</SkillChip>
                ))}
              </SkillsRow>
            </Info>
          </ResultCard>
        );
      })}
    </ResultsContainer>
  );
};

export default MatchResults;
