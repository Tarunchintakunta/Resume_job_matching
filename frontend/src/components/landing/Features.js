import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const FeaturesSection = styled.section`
  padding: ${props => props.theme.spacing.xxl} 0;
  background-color: ${props => props.theme.colors.white};
`;

const SectionTitle = styled(motion.h2)`
  text-align: center;
  font-size: ${props => props.theme.fontSizes.xlarge};
  margin-bottom: ${props => props.theme.spacing.xl};
  color: ${props => props.theme.colors.text};
`;

const FeaturesContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ${props => props.theme.spacing.lg};
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: ${props => props.theme.spacing.xl};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    grid-template-columns: 1fr;
  }
`;

const FeatureCard = styled(motion.div)`
  background-color: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.borderRadius.medium};
  padding: ${props => props.theme.spacing.xl};
  box-shadow: ${props => props.theme.shadows.medium};
  transition: transform ${props => props.theme.transitions.medium};
  
  &:hover {
    transform: translateY(-10px);
  }
`;

const FeatureIcon = styled.div`
  width: 64px;
  height: 64px;
  border-radius: ${props => props.theme.borderRadius.medium};
  background: ${props => props.theme.colors.gradient};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: ${props => props.theme.spacing.md};
  
  svg {
    width: 32px;
    height: 32px;
    color: ${props => props.theme.colors.white};
  }
`;

const FeatureTitle = styled.h3`
  font-size: ${props => props.theme.fontSizes.large};
  margin-bottom: ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.text};
`;

const FeatureDescription = styled.p`
  color: ${props => props.theme.colors.lightText};
  font-size: ${props => props.theme.fontSizes.regular};
`;

const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2
    }
  }
};

const item = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.6 }
  }
};

const Features = () => {
  const features = [
    {
      icon: (
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 7H7V9H9V7Z" fill="currentColor" />
          <path d="M7 13V11H9V13H7Z" fill="currentColor" />
          <path d="M7 15V17H9V15H7Z" fill="currentColor" />
          <path d="M11 15V17H17V15H11Z" fill="currentColor" />
          <path d="M17 13V11H11V13H17Z" fill="currentColor" />
          <path d="M17 7V9H11V7H17Z" fill="currentColor" />
        </svg>
      ),
      title: "AI-Powered Matching",
      description: "Our algorithm uses advanced NLP techniques to match resumes to job requirements with high accuracy."
    },
    {
      icon: (
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M13 15.9C15.2822 15.4367 17 13.419 17 11C17 8.23858 14.7614 6 12 6C9.23858 6 7 8.23858 7 11C7 13.419 8.71776 15.4367 11 15.9V18H8V20H16V18H13V15.9Z" fill="currentColor" />
        </svg>
      ),
      title: "Skill Extraction",
      description: "Automatically extract and standardize skills from resumes and job descriptions for better matching."
    },
    {
      icon: (
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 17L6 14M12 17L18 14M12 17V21M18 14V18L12 21M18 14L12 11M6 14L12 11M6 14V18L12 21M12 11V7M12 7L15 5.5L18 4L19 2H5L6 4L9 5.5L12 7Z" stroke="currentColor" strokeWidth="2" />
        </svg>
      ),
      title: "Resume Management",
      description: "Easily upload, organize, and search through candidate resumes with our intuitive interface."
    },
    {
      icon: (
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M10 13C10.4295 13 10.8394 13.1172 11.2002 13.3343C11.5611 13.5515 11.8494 13.8572 12.0247 14.2286C12.1999 14.5999 12.2546 15.0233 12.1821 15.4338C12.1096 15.8443 11.9129 16.2228 11.6213 16.5213C11.3296 16.8197 10.9553 17.0225 10.5486 17.0994C10.142 17.1763 9.72099 17.1259 9.35269 16.9534C8.9844 16.781 8.68058 16.4939 8.4656 16.1334C8.25062 15.7729 8.13474 15.3628 8.13474 14.9429C8.13474 14.376 8.36262 13.8326 8.7679 13.4282C9.17319 13.0237 9.72099 12.7857 10.2915 12.7857" stroke="currentColor" strokeWidth="2" />
          <path d="M13.7227 10.5714C14.1522 10.5714 14.5621 10.6887 14.9229 10.9058C15.2838 11.1229 15.5721 11.4286 15.7474 11.8C15.9226 12.1714 15.9773 12.5947 15.9048 13.0052C15.8323 13.4157 15.6355 13.7942 15.3439 14.0927C15.0523 14.3912 14.678 14.5939 14.2713 14.6708C13.8647 14.7477 13.4437 14.6973 13.0754 14.5249C12.7071 14.3524 12.4033 14.0654 12.1883 13.7049C11.9733 13.3443 11.8574 12.9343 11.8574 12.5143C11.8574 11.9474 12.0853 11.404 12.4906 10.9996C12.8959 10.5952 13.4437 10.3571 14.0142 10.3571" stroke="currentColor" strokeWidth="2" />
          <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" />
        </svg>
      ),
      title: "Data Analytics",
      description: "Gain insights into your recruitment process with detailed analytics and reporting."
    },
    {
      icon: (
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 8V12L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" />
        </svg>
      ),
      title: "Time-Saving",
      description: "Reduce screening time by up to 75% with automated initial candidate evaluation."
    },
    {
      icon: (
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 11L12 14L20 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M20 12V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V6C4 4.89543 4.89543 4 6 4H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      ),
      title: "Bias Reduction",
      description: "Our algorithm focuses on skills and qualifications, helping to reduce unconscious bias in hiring."
    }
  ];

  return (
    <FeaturesSection id="features">
      <SectionTitle
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
      >
        Powerful Features to Streamline Your Hiring
      </SectionTitle>
      
      <FeaturesContainer
        as={motion.div}
        variants={container}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
      >
        {features.map((feature, index) => (
          <FeatureCard key={index} variants={item}>
            <FeatureIcon>{feature.icon}</FeatureIcon>
            <FeatureTitle>{feature.title}</FeatureTitle>
            <FeatureDescription>{feature.description}</FeatureDescription>
          </FeatureCard>
        ))}
      </FeaturesContainer>
    </FeaturesSection>
  );
};

export default Features;