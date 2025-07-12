import React from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';

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

const Dashboard = () => {
  return (
    <>
      <Header />
      <DashboardContainer>
        <ContentContainer>
          <PageTitle>Dashboard</PageTitle>
          <p>This is the dashboard page. It will display statistics and overview of your resumes, jobs, and matches.</p>
        </ContentContainer>
      </DashboardContainer>
      <Footer />
    </>
  );
};

export default Dashboard;