import React, { useState } from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import JobCreate from '../components/jobs/JobCreate';
import JobList from '../components/jobs/JobList';

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

const JobsPage = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  
  const handleJobCreated = () => {
    // Trigger a refresh of the job list
    setRefreshTrigger(prev => prev + 1);
  };
  
  return (
    <>
      <Header />
      <PageContainer>
        <ContentContainer>
          <PageTitle>Job Postings</PageTitle>
          <p>This page will allow you to create, view, and manage job postings.</p>
          
          <JobCreate onJobCreated={handleJobCreated} />
          <JobList refreshTrigger={refreshTrigger} />
        </ContentContainer>
      </PageContainer>
      <Footer />
    </>
  );
};

export default JobsPage;