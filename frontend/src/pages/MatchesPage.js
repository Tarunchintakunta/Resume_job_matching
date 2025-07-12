import React from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Footer from '../components/common/Footer';

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

const MatchesPage = () => {
  return (
    <>
      <Header />
      <PageContainer>
        <ContentContainer>
          <PageTitle>Match Results</PageTitle>
          <p>This page will display match results between resumes and job postings.</p>
        </ContentContainer>
      </PageContainer>
      <Footer />
    </>
  );
};

export default MatchesPage;