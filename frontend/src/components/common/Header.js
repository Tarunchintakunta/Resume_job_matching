import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import Button from './Button';

const HeaderContainer = styled(motion.header)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: ${props => props.scrolled ? props.theme.colors.white : 'transparent'};
  box-shadow: ${props => props.scrolled ? props.theme.shadows.small : 'none'};
  transition: all ${props => props.theme.transitions.medium};
`;

const NavContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const Logo = styled(Link)`
  font-size: ${props => props.theme.fontSizes.large};
  font-weight: 700;
  color: ${props => props.scrolled ? props.theme.colors.primary : props.theme.colors.white};
  text-decoration: none;
  display: flex;
  align-items: center;
  
  svg {
    margin-right: 0.5rem;
  }
`;

const NavLinks = styled.nav`
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    display: none;
  }
`;

const NavLink = styled(Link)`
  margin: 0 1rem;
  color: ${props => props.scrolled ? props.theme.colors.text : props.theme.colors.white};
  text-decoration: none;
  font-weight: 500;
  position: relative;
  
  &:after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 2px;
    background-color: ${props => props.theme.colors.primary};
    transition: width ${props => props.theme.transitions.fast};
  }
  
  &:hover:after, &.active:after {
    width: 100%;
  }
`;

const MobileMenuButton = styled.button`
  background: transparent;
  border: none;
  color: ${props => props.scrolled ? props.theme.colors.text : props.theme.colors.white};
  font-size: 1.5rem;
  cursor: pointer;
  display: none;
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    display: block;
  }
`;

const MobileMenu = styled(motion.div)`
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 300px;
  background: ${props => props.theme.colors.white};
  box-shadow: ${props => props.theme.shadows.large};
  padding: 2rem;
  display: flex;
  flex-direction: column;
  z-index: 200;
`;

const MobileNavLink = styled(Link)`
  margin: 1rem 0;
  color: ${props => props.theme.colors.text};
  text-decoration: none;
  font-weight: 500;
  font-size: ${props => props.theme.fontSizes.medium};
`;

const Overlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 150;
`;

const Header = ({ isLanding }) => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 50;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [scrolled]);
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <>
      <HeaderContainer
        scrolled={scrolled || !isLanding}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <NavContainer>
          <Logo to="/" scrolled={scrolled || !isLanding}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" fill={scrolled || !isLanding ? "#4361ee" : "#fff"} />
              <path d="M2 17L12 22L22 17" fill={scrolled || !isLanding ? "#4361ee" : "#fff"} />
              <path d="M2 12L12 17L22 12" fill={scrolled || !isLanding ? "#4361ee" : "#fff"} />
            </svg>
            ResumeMatcher
          </Logo>
          
          <NavLinks>
            <NavLink to="/dashboard" scrolled={scrolled || !isLanding} className={isActive('/dashboard') ? 'active' : ''}>
              Dashboard
            </NavLink>
            <NavLink to="/resumes" scrolled={scrolled || !isLanding} className={isActive('/resumes') ? 'active' : ''}>
              Resumes
            </NavLink>
            <NavLink to="/jobs" scrolled={scrolled || !isLanding} className={isActive('/jobs') ? 'active' : ''}>
              Jobs
            </NavLink>
            <NavLink to="/matches" scrolled={scrolled || !isLanding} className={isActive('/matches') ? 'active' : ''}>
              Matches
            </NavLink>
            {isLanding && (
              <Button to="/dashboard" size="small">
                Get Started
              </Button>
            )}
          </NavLinks>
          
          <MobileMenuButton 
            scrolled={scrolled || !isLanding}
            onClick={() => setMobileMenuOpen(true)}
          >
            ☰
          </MobileMenuButton>
        </NavContainer>
      </HeaderContainer>
      
      <AnimatePresence>
        {mobileMenuOpen && (
          <>
            <Overlay 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileMenuOpen(false)}
            />
            <MobileMenu
              initial={{ x: 300 }}
              animate={{ x: 0 }}
              exit={{ x: 300 }}
              transition={{ type: 'spring', damping: 20 }}
            >
              <MobileNavLink to="/dashboard" onClick={() => setMobileMenuOpen(false)}>
                Dashboard
              </MobileNavLink>
              <MobileNavLink to="/resumes" onClick={() => setMobileMenuOpen(false)}>
                Resumes
              </MobileNavLink>
              <MobileNavLink to="/jobs" onClick={() => setMobileMenuOpen(false)}>
                Jobs
              </MobileNavLink>
              <MobileNavLink to="/matches" onClick={() => setMobileMenuOpen(false)}>
                Matches
              </MobileNavLink>
              <Button to="/dashboard" onClick={() => setMobileMenuOpen(false)}>
                Get Started
              </Button>
            </MobileMenu>
          </>
        )}
      </AnimatePresence>
    </>
  );
};

export default Header;