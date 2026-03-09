import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import { getResumes } from '../services/resumeService';
import { getJobs } from '../services/jobService';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

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

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const StatCard = styled(motion.div)`
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const StatIcon = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: ${props => props.bg || 'linear-gradient(90deg, #4361ee, #4895ef)'};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  font-size: 24px;
  color: #fff;
`;

const StatValue = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 4px;
`;

const StatLabel = styled.div`
  font-size: 0.95rem;
  color: #6c757d;
`;

const ChartsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-top: 32px;
  margin-bottom: 32px;

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

const SectionTitle = styled.h2`
  font-size: 1.25rem;
  margin-bottom: 16px;
  margin-top: 32px;
  color: #212529;
`;

const Card = styled.div`
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
`;

const ItemsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const Item = styled.div`
  padding: 14px;
  border-radius: 8px;
  background-color: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ItemInfo = styled.div``;

const ItemTitle = styled.div`
  font-weight: 600;
  margin-bottom: 4px;
`;

const ItemDetail = styled.div`
  font-size: 0.85rem;
  color: #6c757d;
`;

const ViewAllLink = styled.a`
  display: inline-block;
  margin-top: 12px;
  color: #4361ee;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
`;

const Dashboard = () => {
  const [stats, setStats] = useState({ resumes: 0, jobs: 0, matches: 0 });
  const [recentResumes, setRecentResumes] = useState([]);
  const [recentJobs, setRecentJobs] = useState([]);
  const [allResumes, setAllResumes] = useState([]);
  const [allJobs, setAllJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [resumesData, jobsData] = await Promise.all([getResumes(), getJobs()]);
        setAllResumes(resumesData);
        setAllJobs(jobsData);
        setRecentResumes(resumesData.slice(0, 3));
        setRecentJobs(jobsData.slice(0, 3));
        setStats({
          resumes: resumesData.length,
          jobs: jobsData.length,
          matches: 0
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Skills distribution from resumes
  const skillCounts = {};
  allResumes.forEach(r => {
    (r.skills || []).forEach(skill => {
      skillCounts[skill] = (skillCounts[skill] || 0) + 1;
    });
  });
  const topSkills = Object.entries(skillCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);

  const skillsChartData = {
    labels: topSkills.map(([name]) => name),
    datasets: [{
      label: 'Candidates with skill',
      data: topSkills.map(([, count]) => count),
      backgroundColor: [
        'rgba(67, 97, 238, 0.7)',
        'rgba(72, 149, 239, 0.7)',
        'rgba(75, 181, 67, 0.7)',
        'rgba(255, 193, 7, 0.7)',
        'rgba(255, 51, 51, 0.7)',
        'rgba(156, 39, 176, 0.7)',
        'rgba(0, 188, 212, 0.7)',
        'rgba(255, 152, 0, 0.7)',
      ],
      borderRadius: 6,
    }]
  };

  // Job types distribution
  const jobTypeCounts = {};
  allJobs.forEach(j => {
    const type = j.job_type || 'Not specified';
    jobTypeCounts[type] = (jobTypeCounts[type] || 0) + 1;
  });

  const jobTypeData = {
    labels: Object.keys(jobTypeCounts),
    datasets: [{
      data: Object.values(jobTypeCounts),
      backgroundColor: [
        'rgba(67, 97, 238, 0.8)',
        'rgba(75, 181, 67, 0.8)',
        'rgba(255, 193, 7, 0.8)',
        'rgba(255, 51, 51, 0.8)',
        'rgba(156, 39, 176, 0.8)',
      ],
      borderWidth: 2,
      borderColor: '#fff',
    }]
  };

  // Required skills from jobs
  const jobSkillCounts = {};
  allJobs.forEach(j => {
    (j.skills_required || []).forEach(skill => {
      jobSkillCounts[skill] = (jobSkillCounts[skill] || 0) + 1;
    });
  });
  const topJobSkills = Object.entries(jobSkillCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);

  const demandChartData = {
    labels: topJobSkills.map(([name]) => name),
    datasets: [{
      label: 'Jobs requiring skill',
      data: topJobSkills.map(([, count]) => count),
      borderColor: 'rgb(67, 97, 238)',
      backgroundColor: 'rgba(67, 97, 238, 0.1)',
      fill: true,
      tension: 0.4,
      pointRadius: 5,
      pointBackgroundColor: 'rgb(67, 97, 238)',
    }]
  };

  // Experience distribution
  const expCounts = { '0-1': 0, '1-3': 0, '3-5': 0, '5+': 0 };
  allResumes.forEach(r => {
    const expLen = (r.experience || []).length;
    if (expLen <= 1) expCounts['0-1']++;
    else if (expLen <= 3) expCounts['1-3']++;
    else if (expLen <= 5) expCounts['3-5']++;
    else expCounts['5+']++;
  });

  const expChartData = {
    labels: Object.keys(expCounts),
    datasets: [{
      data: Object.values(expCounts),
      backgroundColor: [
        'rgba(255, 193, 7, 0.8)',
        'rgba(72, 149, 239, 0.8)',
        'rgba(67, 97, 238, 0.8)',
        'rgba(75, 181, 67, 0.8)',
      ],
      borderWidth: 2,
      borderColor: '#fff',
    }]
  };

  const hasData = allResumes.length > 0 || allJobs.length > 0;

  return (
    <>
      <Header />
      <DashboardContainer>
        <ContentContainer>
          <PageTitle>Dashboard</PageTitle>

          <StatsContainer>
            <StatCard whileHover={{ y: -5 }} transition={{ duration: 0.3 }}>
              <StatIcon bg="linear-gradient(135deg, #4361ee, #4895ef)">
                <span role="img" aria-label="resume">&#128196;</span>
              </StatIcon>
              <StatValue>{stats.resumes}</StatValue>
              <StatLabel>Resumes</StatLabel>
            </StatCard>
            <StatCard whileHover={{ y: -5 }} transition={{ duration: 0.3 }}>
              <StatIcon bg="linear-gradient(135deg, #4bb543, #36a336)">
                <span role="img" aria-label="jobs">&#128188;</span>
              </StatIcon>
              <StatValue>{stats.jobs}</StatValue>
              <StatLabel>Job Postings</StatLabel>
            </StatCard>
            <StatCard whileHover={{ y: -5 }} transition={{ duration: 0.3 }}>
              <StatIcon bg="linear-gradient(135deg, #ffc107, #e6a800)">
                <span role="img" aria-label="matches">&#129309;</span>
              </StatIcon>
              <StatValue>{stats.matches}</StatValue>
              <StatLabel>Matches</StatLabel>
            </StatCard>
          </StatsContainer>

          {hasData && (
            <ChartsGrid>
              {topSkills.length > 0 && (
                <ChartCard>
                  <ChartTitle>Top Skills in Resumes</ChartTitle>
                  <Bar
                    data={skillsChartData}
                    options={{
                      responsive: true,
                      plugins: { legend: { display: false } },
                      scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1 } },
                        x: { ticks: { maxRotation: 45, font: { size: 11 } } }
                      }
                    }}
                  />
                </ChartCard>
              )}

              {Object.keys(jobTypeCounts).length > 0 && (
                <ChartCard>
                  <ChartTitle>Job Types Distribution</ChartTitle>
                  <Doughnut
                    data={jobTypeData}
                    options={{
                      responsive: true,
                      plugins: { legend: { position: 'bottom' } }
                    }}
                  />
                </ChartCard>
              )}

              {topJobSkills.length > 0 && (
                <ChartCard>
                  <ChartTitle>Most In-Demand Skills (from Jobs)</ChartTitle>
                  <Line
                    data={demandChartData}
                    options={{
                      responsive: true,
                      plugins: { legend: { display: false } },
                      scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1 } },
                        x: { ticks: { maxRotation: 45, font: { size: 11 } } }
                      }
                    }}
                  />
                </ChartCard>
              )}

              {allResumes.length > 0 && (
                <ChartCard>
                  <ChartTitle>Experience Level Distribution</ChartTitle>
                  <Doughnut
                    data={expChartData}
                    options={{
                      responsive: true,
                      plugins: { legend: { position: 'bottom' } }
                    }}
                  />
                </ChartCard>
              )}
            </ChartsGrid>
          )}

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
                        <ItemDetail>{resume.email} &bull; {resume.skills?.length || 0} skills</ItemDetail>
                      </ItemInfo>
                    </Item>
                  ))}
                </ItemsList>
                <ViewAllLink href="/resumes">View all resumes &rarr;</ViewAllLink>
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
                        <ItemDetail>{job.company} &bull; {job.location}</ItemDetail>
                      </ItemInfo>
                    </Item>
                  ))}
                </ItemsList>
                <ViewAllLink href="/jobs">View all job postings &rarr;</ViewAllLink>
              </>
            ) : (
              <p>No job postings found. Create a job posting to get started.</p>
            )}
          </Card>
        </ContentContainer>
      </DashboardContainer>
      <Footer />
    </>
  );
};

export default Dashboard;
