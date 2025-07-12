import React, { useState } from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';
import ResumeUpload from '../components/resumes/ResumeUpload';
import ResumeList from '../components/resumes/ResumeList';

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

const ResumesPage = () => {
  const [selectedResume, setSelectedResume] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  
  const handleResumeSelect = (resume) => {
    setSelectedResume(resume);
  };
  
  const handleUploadSuccess = () => {
    // Trigger a refresh of the resume list
    setRefreshTrigger(prev => prev + 1);
  };
  
  return (
    <>
      <Header />
      <PageContainer>
        <ContentContainer>
          <PageTitle>Resume Management</PageTitle>
          <p>This page will allow you to upload, view, and manage candidate resumes.</p>
          
          <ResumeUpload onUploadSuccess={handleUploadSuccess} />
          <ResumeList 
            onResumeSelect={handleResumeSelect} 
            refreshTrigger={refreshTrigger} 
          />
        </ContentContainer>
      </PageContainer>
      <Footer />
    </>
  );
};

export default ResumesPage;