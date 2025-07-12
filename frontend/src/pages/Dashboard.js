import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import { getResumes } from '../services/resumeService';
import { getJobs } from '../services/jobService';

const DashboardContainer = styled.div`
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

const StatsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: ${props => props.theme.spacing.lg};
  margin-bottom: ${props => props.theme.spacing.xl};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
  }
`;

const StatCard = styled(motion.div)`
  background-color: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.borderRadius.medium};
  padding: ${props => props.theme.spacing.lg};
  box-shadow: ${props => props.theme.shadows.medium};
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const StatIcon = styled.div`
  width: 60px;
  height: 60px;
  border-radius: ${props => props.theme.borderRadius.round};
  background: ${props => props.theme.colors.gradient};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: ${props => props.theme.spacing.md};
  
  i {
    font-size: 24px;
    color: ${props => props.theme.colors.white};
  }
`;

const StatValue = styled.div`
  font-size: ${props => props.theme.fontSizes.xxlarge};
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const StatLabel = styled.div`
  font-size: ${props => props.theme.fontSizes.medium};
  color: ${props => props.theme.colors.lightText};
`;

const RecentContainer = styled.div`
  margin-top: ${props => props.theme.spacing.xl};
`;

const SectionTitle = styled.h2`
  font-size: ${props => props.theme.fontSizes.large};
  margin-bottom: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.text};
`;

const Card = styled.div`
  background-color: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.borderRadius.medium};
  padding: ${props => props.theme.spacing.lg};
  box-shadow: ${props => props.theme.shadows.medium};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const ItemsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const Item = styled.div`
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.small};
  background-color: ${props => props.theme.colors.background};
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ItemInfo = styled.div``;

const ItemTitle = styled.div`
  font-weight: 600;
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const ItemDetail = styled.div`
  font-size: ${props => props.theme.fontSizes.small};
  color: ${props => props.theme.colors.lightText};
`;

const ViewAllLink = styled.a`
  display: inline-block;
  margin-top: ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.primary};
  font-weight: 500;
  cursor: pointer;
  
  &:hover {
    text-decoration: underline;
  }
`;

const Dashboard = () => {
  const [stats, setStats] = useState({
    resumes: 0,
    jobs: 0,
    matches: 0
  });
  
  const [recentResumes, setRecentResumes] = useState([]);
  const [recentJobs, setRecentJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch resumes
        const resumesData = await getResumes();
        setRecentResumes(resumesData.slice(0, 3)); // Get 3 most recent
        
        // Fetch jobs
        const jobsData = await getJobs();
        setRecentJobs(jobsData.slice(0, 3)); // Get 3 most recent
        
        // Update stats
        setStats({
          resumes: resumesData.length,
          jobs: jobsData.length,
          matches: 0 // Will be updated when we implement matches
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);
  
  return (
    <>
      <Header />
      <DashboardContainer>
        <ContentContainer>
          <PageTitle>Dashboard</PageTitle>
          
          <StatsContainer>
            <StatCard
              whileHover={{ y: -5 }}
              transition={{ duration: 0.3 }}
            >
              <StatIcon>
                <i className="fas fa-file-alt"></i>
              </StatIcon>
              <StatValue>{stats.resumes}</StatValue>
              <StatLabel>Resumes</StatLabel>
            </StatCard>
            
            <StatCard
              whileHover={{ y: -5 }}
              transition={{ duration: 0.3 }}
            >
              <StatIcon>
                <i className="fas fa-briefcase"></i>
              </StatIcon>
              <StatValue>{stats.jobs}</StatValue>
              <StatLabel>Job Postings</StatLabel>
            </StatCard>
            
            <StatCard
              whileHover={{ y: -5 }}
              transition={{ duration: 0.3 }}
            >
              <StatIcon>
                <i className="fas fa-handshake"></i>
              </StatIcon>
              <StatValue>{stats.matches}</StatValue>
              <StatLabel>Matches</StatLabel>
            </StatCard>
          </StatsContainer>
          
          <RecentContainer>
            <SectionTitle>Recent Resumes</SectionTitle>
            <Card>
              {loading ? (
                <p>Loading recent resumes...</p>
              ) : recentResumes.length > 0 ? (
                <>
                  <ItemsList>
                    {recentResumes.map((resume) => (
                      <Item key={resume.id}>
                        <ItemInfo>
                          <ItemTitle>{resume.name}</ItemTitle>
                          <ItemDetail>{resume.email} • {resume.skills?.length || 0} skills</ItemDetail>
                        </ItemInfo>
                      </Item>
                    ))}
                  </ItemsList>
                  <ViewAllLink href="/resumes">View all resumes →</ViewAllLink>
                </>
              ) : (
                <p>No resumes found. Upload a resume to get started.</p>
              )}
            </Card>
            
            <SectionTitle>Recent Job Postings</SectionTitle>
            <Card>
              {loading ? (
                <p>Loading recent job postings...</p>
              ) : recentJobs.length > 0 ? (
                <>
                  <ItemsList>
                    {recentJobs.map((job) => (
                      <Item key={job.id}>
                        <ItemInfo>
                          <ItemTitle>{job.title}</ItemTitle>
                          <ItemDetail>{job.company} • {job.location}</ItemDetail>
                        </ItemInfo>
                      </Item>
                    ))}
                  </ItemsList>
                  <ViewAllLink href="/jobs">View all job postings →</ViewAllLink>
                </>
              ) : (
                <p>No job postings found. Create a job posting to get started.</p>
              )}
            </Card>
          </RecentContainer>
        </ContentContainer>
      </DashboardContainer>
      <Footer />
    </>
  );
};

export default Dashboard;