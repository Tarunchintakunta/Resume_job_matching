import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';

const FooterContainer = styled.footer`
  background-color: ${props => props.theme.colors.darkGray};
  color: ${props => props.theme.colors.lightGray};
  padding: ${props => props.theme.spacing.xl} 0;
`;

const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ${props => props.theme.spacing.lg};
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: ${props => props.theme.spacing.lg};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
  }
`;

const FooterColumn = styled.div`
  display: flex;
  flex-direction: column;
`;

const FooterHeading = styled.h3`
  color: ${props => props.theme.colors.white};
  margin-bottom: ${props => props.theme.spacing.md};
  font-size: ${props => props.theme.fontSizes.medium};
`;

const FooterLink = styled(Link)`
  color: ${props => props.theme.colors.lightGray};
  margin-bottom: ${props => props.theme.spacing.sm};
  transition: color ${props => props.theme.transitions.fast};
  
  &:hover {
    color: ${props => props.theme.colors.white};
  }
`;

const FooterText = styled.p`
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const SocialLinks = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  margin-top: ${props => props.theme.spacing.sm};
`;

const SocialIcon = styled.a`
  color: ${props => props.theme.colors.lightGray};
  font-size: ${props => props.theme.fontSizes.large};
  transition: color ${props => props.theme.transitions.fast};
  
  &:hover {
    color: ${props => props.theme.colors.white};
  }
`;

const Copyright = styled.div`
  text-align: center;
  padding-top: ${props => props.theme.spacing.lg};
  margin-top: ${props => props.theme.spacing.lg};
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: ${props => props.theme.spacing.lg};
  padding-right: ${props => props.theme.spacing.lg};
`;

const Footer = () => {
  return (
    <FooterContainer>
      <FooterContent>
        <FooterColumn>
          <FooterHeading>ResumeMatcher</FooterHeading>
          <FooterText>
            Intelligent resume-to-job matching system powered by AI to streamline your recruitment process.
          </FooterText>
          <SocialLinks>
            <SocialIcon href="#" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-twitter"></i>
            </SocialIcon>
            <SocialIcon href="#" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-linkedin-in"></i>
            </SocialIcon>
            <SocialIcon href="#" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-github"></i>
            </SocialIcon>
          </SocialLinks>
        </FooterColumn>
        
        <FooterColumn>
          <FooterHeading>Features</FooterHeading>
          <FooterLink to="/resumes">Resume Management</FooterLink>
          <FooterLink to="/jobs">Job Postings</FooterLink>
          <FooterLink to="/matches">AI Matching</FooterLink>
          <FooterLink to="/dashboard">Analytics</FooterLink>
        </FooterColumn>
        
        <FooterColumn>
          <FooterHeading>Resources</FooterHeading>
          <FooterLink to="#">Documentation</FooterLink>
          <FooterLink to="#">API</FooterLink>
          <FooterLink to="#">Support</FooterLink>
          <FooterLink to="#">FAQ</FooterLink>
        </FooterColumn>
        
        <FooterColumn>
          <FooterHeading>Company</FooterHeading>
          <FooterLink to="#">About Us</FooterLink>
          <FooterLink to="#">Contact</FooterLink>
          <FooterLink to="#">Privacy Policy</FooterLink>
          <FooterLink to="#">Terms of Service</FooterLink>
        </FooterColumn>
      </FooterContent>
      
      <Copyright>
        <FooterText>© 2025 ResumeMatcher. All rights reserved.</FooterText>
      </Copyright>
    </FooterContainer>
  );
};

export default Footer;