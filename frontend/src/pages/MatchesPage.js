import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import { getJobs } from '../services/jobService';
import { getResumes } from '../services/resumeService';
import { calculateMatches, getMatchesForJob } from '../services/matchService';
import Button from '../components/common/Button';

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

const Card = styled(motion.div)`
  background-color: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.borderRadius.medium};
  padding: ${props => props.theme.spacing.xl};
  box-shadow: ${props => props.theme.shadows.medium};
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const SectionTitle = styled.h2`
  font-size: ${props => props.theme.fontSizes.large};
  margin-bottom: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.text};
`;

const FormGroup = styled.div`
  margin-bottom: ${props => props.theme.spacing.md};
`;

const Label = styled.label`
  display: block;
  margin-bottom: ${props => props.theme.spacing.sm};
  font-weight: 500;
  color: ${props => props.theme.colors.text};
`;

const Select = styled.select`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: ${props => props.theme.fontSizes.regular};
  transition: border-color ${props => props.theme.transitions.fast};
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
    outline: none;
  }
`;

const ButtonContainer = styled.div`
  margin-top: ${props => props.theme.spacing.lg};
`;

const MatchList = styled.div`
  margin-top: ${props => props.theme.spacing.lg};
`;

const MatchItem = styled(motion.div)`
  padding: ${props => props.theme.spacing.lg};
  border-radius: ${props => props.theme.borderRadius.small};
  margin-bottom: ${props => props.theme.spacing.md};
  background-color: ${props => props.theme.colors.background};
  display: flex;
  align-items: center;
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    flex-direction: column;
    align-items: flex-start;
  }
`;

const MatchScore = styled.div`
  width: 80px;
  height: 80px;
  border-radius: ${props => props.theme.borderRadius.round};
  background: ${props => props.theme.colors.gradient};
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.xlarge};
  font-weight: 700;
  margin-right: ${props => props.theme.spacing.lg};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    margin-bottom: ${props => props.theme.spacing.md};
  }
`;

const MatchInfo = styled.div`
  flex: 1;
`;

const MatchName = styled.h3`
  font-size: ${props => props.theme.fontSizes.medium};
  margin-bottom: ${props => props.theme.spacing.xs};
  color: ${props => props.theme.colors.text};
`;

const MatchDetail = styled.div`
  font-size: ${props => props.theme.fontSizes.small};
  color: ${props => props.theme.colors.lightText};
  margin-bottom: ${props => props.theme.spacing.sm};
  
  i {
    margin-right: ${props => props.theme.spacing.xs};
  }
`;

const SkillsMatch = styled.div`
  margin-top: ${props => props.theme.spacing.sm};
`;

const SkillsTitle = styled.div`
  font-weight: 500;
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const SkillTags = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: ${props => props.theme.spacing.xs};
`;

const SkillTag = styled.span`
  background-color: ${props => props.matched 
    ? 'rgba(75, 181, 67, 0.1)' 
    : 'rgba(255, 51, 51, 0.1)'};
  color: ${props => props.matched 
    ? props.theme.colors.success 
    : props.theme.colors.error};
  font-size: ${props => props.theme.fontSizes.small};
  padding: 2px 8px;
  border-radius: ${props => props.theme.borderRadius.small};
  
  i {
    margin-right: 4px;
  }
`;

const Loader = styled.div`
  text-align: center;
  padding: ${props => props.theme.spacing.xl} 0;
  color: ${props => props.theme.colors.lightText};
  
  i {
    font-size: ${props => props.theme.fontSizes.xlarge};
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: ${props => props.theme.spacing.xl} 0;
  color: ${props => props.theme.colors.lightText};
`;

const MatchesPage = () => {
  const [jobs, setJobs] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [selectedJobId, setSelectedJobId] = useState('');
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch jobs
        const jobsData = await getJobs();
        setJobs(jobsData);
        
        // Fetch resumes
        const resumesData = await getResumes();
        setResumes(resumesData);
        
        // Set default selected job if any jobs exist
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
  
  const getResumeById = (resumeId) => {
    return resumes.find(resume => resume.id === resumeId) || {};
  };
  
  return (
    <>
      <Header />
      <PageContainer>
        <ContentContainer>
          <PageTitle>Match Results</PageTitle>
          
          <Card
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <SectionTitle>Calculate Matches</SectionTitle>
            
            <FormGroup>
              <Label htmlFor="job-select">Select Job Posting</Label>
              <Select
                id="job-select"
                value={selectedJobId}
                onChange={(e) => setSelectedJobId(e.target.value)}
              >
                <option value="">-- Select a job posting --</option>
                {jobs.map((job) => (
                  <option key={job.id} value={job.id}>
                    {job.title} at {job.company}
                  </option>
                ))}
              </Select>
            </FormGroup>
            
            <ButtonContainer>
              <Button 
                onClick={handleCalculateMatches} 
                disabled={!selectedJobId || loading}
              >
                {loading ? 'Calculating...' : 'Calculate Matches'}
              </Button>
            </ButtonContainer>
          </Card>
          
          {loading ? (
            <Loader>
              <i className="fas fa-spinner"></i>
              <p>Calculating matches...</p>
            </Loader>
          ) : matches.length > 0 ? (
            <MatchList>
              <SectionTitle>Match Results</SectionTitle>
              
              {matches.map((match, index) => {
                const resume = getResumeById(match.resume_id);
                const scorePercentage = Math.round(match.score * 100);
                
                return (
                  <MatchItem
                    key={match.id || index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                  >
                    <MatchScore>{scorePercentage}%</MatchScore>
                    <MatchInfo>
                      <MatchName>{resume.name || 'Unknown Candidate'}</MatchName>
                      <MatchDetail>
                        <i className="fas fa-envelope"></i> {resume.email || 'No email'}
                      </MatchDetail>
                      <MatchDetail>
                        <i className="fas fa-briefcase"></i> {resume.experience?.length || 0} experience entries
                      </MatchDetail>
                      
                      <SkillsMatch>
                        <SkillsTitle>Skills Match:</SkillsTitle>
                        <SkillTags>
                          {match.details?.matching_skills?.map((skill, i) => (
                            <SkillTag key={i} matched={true}>
                              <i className="fas fa-check"></i> {skill}
                            </SkillTag>
                          ))}
                          
                          {match.details?.missing_skills?.slice(0, 3).map((skill, i) => (
                            <SkillTag key={i} matched={false}>
                              <i className="fas fa-times"></i> {skill}
                            </SkillTag>
                          ))}
                          
                          {match.details?.missing_skills?.length > 3 && (
                            <SkillTag matched={false}>
                              +{match.details.missing_skills.length - 3} more missing
                            </SkillTag>
                          )}
                        </SkillTags>
                      </SkillsMatch>
                    </MatchInfo>
                  </MatchItem>
                );
              })}
            </MatchList>
          ) : selectedJobId && !loading && (
            <EmptyState>
              <i className="fas fa-search" style={{ fontSize: '3rem', marginBottom: '1rem' }}></i>
              <p>No matches found. Try selecting a different job or upload more resumes.</p>
            </EmptyState>
          )}
        </ContentContainer>
      </PageContainer>
      <Footer />
    </>
  );
};

export default MatchesPage;