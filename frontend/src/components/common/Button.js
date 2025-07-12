import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const StyledButton = styled(motion.button)`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  background: ${props => props.variant === 'outlined' 
    ? 'transparent' 
    : props.theme.colors.gradient};
  color: ${props => props.variant === 'outlined' 
    ? props.theme.colors.primary 
    : props.theme.colors.white};
  border: 2px solid ${props => props.variant === 'outlined' 
    ? props.theme.colors.primary 
    : 'transparent'};
  border-radius: ${props => props.theme.borderRadius.medium};
  font-weight: 600;
  font-size: ${props => props.size === 'large' 
    ? props.theme.fontSizes.medium 
    : props.theme.fontSizes.regular};
  cursor: pointer;
  transition: all ${props => props.theme.transitions.fast};
  box-shadow: ${props => props.variant === 'outlined' 
    ? 'none' 
    : props.theme.shadows.button};
  text-decoration: none;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.variant === 'outlined' 
      ? 'none' 
      : '0 6px 20px rgba(67, 97, 238, 0.4)'};
  }
  
  &:active {
    transform: translateY(0);
  }
  
  svg {
    margin-left: ${props => props.theme.spacing.sm};
  }
`;

const LinkButton = styled(StyledButton).attrs({ as: motion(Link) })``;

const Button = ({ children, to, variant, size, onClick, ...props }) => {
  if (to) {
    return (
      <LinkButton 
        to={to} 
        variant={variant} 
        size={size} 
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.98 }}
        {...props}
      >
        {children}
      </LinkButton>
    );
  }
  
  return (
    <StyledButton 
      variant={variant} 
      size={size} 
      onClick={onClick}
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.98 }}
      {...props}
    >
      {children}
    </StyledButton>
  );
};

export default Button;