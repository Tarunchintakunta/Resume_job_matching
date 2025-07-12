import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Button from '../common/Button';

const CTASection = styled.section`
  padding: ${props => props.theme.spacing.xxl} 0;
  background: ${props => props.theme.colors.gradient};
  color: ${props => props.theme.colors.white};
  text-align: center;
  position: relative;
  overflow: hidden;
`;

const ShapeContainer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
`;

const Shape = styled(motion.div)`
  position: absolute;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: ${props => props.theme.borderRadius.round};
`;

const ContentContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 0 ${props => props.theme.spacing.lg};
  position: relative;
  z-index: 1;
`;

const CTATitle = styled(motion.h2)`
  font-size: ${props => props.theme.fontSizes.xlarge};
  margin-bottom: ${props => props.theme.spacing.lg};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: ${props => props.theme.fontSizes.large};
  }
`;

const CTADescription = styled(motion.p)`
  font-size: ${props => props.theme.fontSizes.medium};
  margin-bottom: ${props => props.theme.spacing.xl};
  opacity: 0.9;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: ${props => props.theme.fontSizes.regular};
  }
`;

const ButtonContainer = styled(motion.div)`
  display: flex;
  justify-content: center;
  gap: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    align-items: center;
  }
`;

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

const CallToAction = () => {
  return (
    <CTASection>
      <ShapeContainer>
        <Shape
          style={{ width: '250px', height: '250px', top: '-50px', right: '-50px' }}
          animate={{
            x: [0, -30, 0],
            y: [0, 50, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
        <Shape
          style={{ width: '150px', height: '150px', bottom: '50px', left: '10%' }}
          animate={{
            x: [0, 50, 0],
            y: [0, -30, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
      </ShapeContainer>
      
      <ContentContainer>
        <CTATitle
          initial="hidden"
          whileInView="visible"
          variants={fadeIn}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          Ready to Transform Your Hiring Process?
        </CTATitle>
        <CTADescription
          initial="hidden"
          whileInView="visible"
          variants={fadeIn}
          transition={{ duration: 0.6, delay: 0.2 }}
          viewport={{ once: true }}
        >
          Start matching the right candidates to your job openings today with our AI-powered system.
          Reduce hiring time, improve quality of hire, and make better hiring decisions.
        </CTADescription>
        <ButtonContainer
          initial="hidden"
          whileInView="visible"
          variants={fadeIn}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
        >
          <Button to="/dashboard" size="large" style={{ background: 'white', color: '#4361ee' }}>
            Get Started Now
          </Button>
          <Button to="#" variant="outlined" size="large">
            Schedule a Demo
          </Button>
        </ButtonContainer>
      </ContentContainer>
    </CTASection>
  );
};

export default CallToAction;