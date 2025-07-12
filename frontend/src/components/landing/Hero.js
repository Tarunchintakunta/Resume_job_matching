import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Button from '../common/Button';

const HeroSection = styled.section`
  height: 100vh;
  min-height: 600px;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: ${props => props.theme.colors.gradient};
  padding-top: 80px;
`;

const HeroContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ${props => props.theme.spacing.lg};
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${props => props.theme.spacing.xl};
  align-items: center;
  position: relative;
  z-index: 1;
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
    text-align: center;
  }
`;

const TextContainer = styled.div`
  color: ${props => props.theme.colors.white};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    order: 2;
  }
`;

const HeroTitle = styled(motion.h1)`
  font-size: ${props => props.theme.fontSizes.xxlarge};
  font-weight: 700;
  margin-bottom: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    font-size: ${props => props.theme.fontSizes.xlarge};
  }
`;

const HeroSubtitle = styled(motion.p)`
  font-size: ${props => props.theme.fontSizes.medium};
  margin-bottom: ${props => props.theme.spacing.lg};
  opacity: 0.9;
`;

const ButtonContainer = styled(motion.div)`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    justify-content: center;
  }
`;

const ImageContainer = styled(motion.div)`
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    order: 1;
    margin-bottom: ${props => props.theme.spacing.lg};
  }
`;

const HeroImage = styled(motion.img)`
  width: 100%;
  max-width: 600px;
`;

const BackgroundShapes = styled.div`
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

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

const Hero = () => {
  return (
    <HeroSection>
      <BackgroundShapes>
        <Shape
          style={{ width: '300px', height: '300px', top: '-100px', left: '-100px' }}
          animate={{
            x: [0, 50, 0],
            y: [0, 30, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
        <Shape
          style={{ width: '200px', height: '200px', bottom: '100px', right: '100px' }}
          animate={{
            x: [0, -30, 0],
            y: [0, -50, 0],
          }}
          transition={{
            duration: 18,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
        <Shape
          style={{ width: '150px', height: '150px', bottom: '-50px', left: '30%' }}
          animate={{
            x: [0, 30, 0],
            y: [0, 30, 0],
          }}
          transition={{
            duration: 12,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
      </BackgroundShapes>
      
      <HeroContent>
        <TextContainer>
          <HeroTitle
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            transition={{ duration: 0.6 }}
          >
            Match the Right Talent to the Right Job
          </HeroTitle>
          <HeroSubtitle
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Streamline your hiring process with our AI-powered resume-to-job matching system.
            Find the best candidates faster and more accurately.
          </HeroSubtitle>
          <ButtonContainer
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Button to="/dashboard" size="large">
              Get Started
            </Button>
            <Button to="#features" variant="outlined" size="large">
              Learn More
            </Button>
          </ButtonContainer>
        </TextContainer>
        
        <ImageContainer
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
        >
          <HeroImage 
            src="/assets/images/hero-image.svg" 
            alt="Resume matching illustration"
            initial={{ y: 20 }}
            animate={{ y: [20, -20, 20] }}
            transition={{
              duration: 6,
              repeat: Infinity,
              repeatType: 'reverse',
              ease: 'easeInOut'
            }}
          />
        </ImageContainer>
      </HeroContent>
    </HeroSection>
  );
};

export default Hero;