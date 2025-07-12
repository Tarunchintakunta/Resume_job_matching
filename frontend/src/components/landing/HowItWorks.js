import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const HowItWorksSection = styled.section`
  padding: ${props => props.theme.spacing.xxl} 0;
  background-color: ${props => props.theme.colors.background};
`;

const SectionTitle = styled(motion.h2)`
  text-align: center;
  font-size: ${props => props.theme.fontSizes.xlarge};
  margin-bottom: ${props => props.theme.spacing.xl};
  color: ${props => props.theme.colors.text};
`;

const StepsContainer = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 ${props => props.theme.spacing.lg};
`;

const Step = styled(motion.div)`
  display: flex;
  margin-bottom: ${props => props.theme.spacing.xl};
  position: relative;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
  }
  
  &:last-child {
    margin-bottom: 0;
  }
  
  &:not(:last-child):before {
    content: '';
    position: absolute;
    top: 80px;
    left: 40px;
    height: calc(100% - 40px);
    width: 2px;
    background-color: ${props => props.theme.colors.primary};
    
    @media (max-width: ${props => props.theme.breakpoints.mobile}) {
      left: 35px;
      height: calc(100% - 60px);
    }
  }
`;

const StepNumber = styled.div`
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
  flex-shrink: 0;
  margin-right: ${props => props.theme.spacing.lg};
  box-shadow: ${props => props.theme.shadows.medium};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    width: 70px;
    height: 70px;
    margin-bottom: ${props => props.theme.spacing.md};
  }
`;

const StepContent = styled.div`
  padding-top: ${props => props.theme.spacing.sm};
`;

const StepTitle = styled.h3`
  font-size: ${props => props.theme.fontSizes.large};
  margin-bottom: ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.text};
`;

const StepDescription = styled.p`
  color: ${props => props.theme.colors.lightText};
  font-size: ${props => props.theme.fontSizes.regular};
  margin-bottom: ${props => props.theme.spacing.md};
`;

const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3
    }
  }
};

const item = {
  hidden: { x: -20, opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: { duration: 0.6 }
  }
};

const HowItWorks = () => {
  const steps = [
    {
      number: 1,
      title: "Upload Resumes",
      description: "Upload candidate resumes in PDF or JSON format. Our system automatically extracts skills, experience, and qualifications."
    },
    {
      number: 2,
      title: "Create Job Postings",
      description: "Create detailed job postings with requirements, qualifications, and desired skills. The more detailed, the better the matches."
    },
    {
      number: 3,
      title: "Run AI Matching",
      description: "Our AI algorithm analyzes resumes against job requirements, calculating match scores based on skills, experience, and overall fit."
    },
    {
      number: 4,
      title: "Review Ranked Candidates",
      description: "Review a ranked list of candidates with detailed match reports showing why each candidate is a good fit for the position."
    }
  ];

  return (
    <HowItWorksSection id="how-it-works">
      <SectionTitle
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
      >
        How It Works
      </SectionTitle>
      
      <StepsContainer
        as={motion.div}
        variants={container}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        {steps.map((step) => (
          <Step key={step.number} variants={item}>
            <StepNumber>{step.number}</StepNumber>
            <StepContent>
              <StepTitle>{step.title}</StepTitle>
              <StepDescription>{step.description}</StepDescription>
            </StepContent>
          </Step>
        ))}
      </StepsContainer>
    </HowItWorksSection>
  );
};

export default HowItWorks;