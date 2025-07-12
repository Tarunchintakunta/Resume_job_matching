import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { getJobs, deleteJob } from '../../services/jobService';
import Button from '../common/Button';

const ListContainer = styled(motion.div)`
  background-color: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.borderRadius.medium};
  padding: ${props => props.theme.spacing.xl};
  box-shadow: ${props => props.theme.shadows.medium};
`;

const Title = styled.h2`
  font-size: ${props => props.theme.fontSizes.large};
  margin-bottom: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.text};
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const JobCount = styled.span`
  font-size: ${props => props.theme.fontSizes.regular};
  color: ${props => props.theme.colors.lightText};
  font-weight: normal;
`;

const JobItem = styled(motion.div)`
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.small};
  margin-bottom: ${props => props.theme.spacing.md};
  background-color: ${props => props.theme.colors.background};
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all ${props => props.theme.transitions.fast};
  
  &:hover {
    box-shadow: ${props => props.theme.shadows.small};
    transform: translateY(-2px);
  }
`;

const JobInfo = styled.div`
  flex: 1;
`;

const JobTitle = styled.h3`
  font-size: ${props => props.theme.fontSizes.medium};
  margin-bottom: ${props => props.theme.spacing.xs};
  color: ${props => props.theme.colors.text};
`;

const JobDetail = styled.div`
  font-size: ${props => props.theme.fontSizes.small};
  color: ${props => props.theme.colors.lightText};
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  
  i {
    margin-right: ${props => props.theme.spacing.xs};
  }
  
  & > * {
    margin-right: ${props => props.theme.spacing.md};
    margin-bottom: ${props => props.theme.spacing.xs};
  }
`;

const SkillTags = styled.div`
  display: flex;
  flex-wrap: wrap;
  margin-top: ${props => props.theme.spacing.xs};
  gap: ${props => props.theme.spacing.xs};
`;

const SkillTag = styled.span`
  background-color: rgba(67, 97, 238, 0.1);
  color: ${props => props.theme.colors.primary};
  font-size: ${props => props.theme.fontSizes.small};
  padding: 2px 8px;
  border-radius: ${props => props.theme.borderRadius.small};
`;

const ActionButtons = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.sm};
`;

const ActionButton = styled.button`
  background: none;
  border: none;
  color: ${props => props.color || props.theme.colors.primary};
  cursor: pointer;
  font-size: ${props => props.theme.fontSizes.regular};
  transition: all ${props => props.theme.transitions.fast};
  
  &:hover {
    opacity: 0.8;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: ${props => props.theme.spacing.xl} 0;
  color: ${props => props.theme.colors.lightText};
`;

const Loader = styled.div`
  text-align: center;
  padding: ${props => props.theme.spacing.xl} 0;
  color: ${props => props.theme.colors.lightText};
  
  i {
    font-size: ${props => props.theme.fontSizes.xlarge};
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const Error = styled.div`
  color: ${props => props.theme.colors.error};
  padding: ${props => props.theme.spacing.md};
  text-align: center;
  margin: ${props => props.theme.spacing.md} 0;
`;

const Pagination = styled.div`
  display: flex;
  justify-content: center;
  margin-top: ${props => props.theme.spacing.lg};
  gap: ${props => props.theme.spacing.sm};
`;

const PaginationButton = styled.button`
  background: ${props => props.active ? props.theme.colors.primary : props.theme.colors.lightGray};
  color: ${props => props.active ? props.theme.colors.white : props.theme.colors.text};
  border: none;
  width: 36px;
  height: 36px;
  border-radius: ${props => props.theme.borderRadius.small};
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  opacity: ${props => props.disabled ? 0.5 : 1};
  
  &:hover:not(:disabled) {
    background: ${props => props.active ? props.theme.colors.primary : props.theme.colors.darkGray};
  }
`;

const JobList = ({ onJobSelect, refreshTrigger = 0 }) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const data = await getJobs();
      setJobs(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch jobs. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [refreshTrigger]);

  const handleDeleteJob = async (id, e) => {
    e.stopPropagation(); // Prevent triggering the click on the parent div
    
    if (window.confirm('Are you sure you want to delete this job posting?')) {
      try {
        await deleteJob(id);
        fetchJobs(); // Refresh the list
      } catch (err) {
        setError('Failed to delete job posting. Please try again.');
      }
    }
  };

  const handleJobClick = (job) => {
    if (onJobSelect) {
      onJobSelect(job);
    }
  };

  // Pagination logic
  const totalPages = Math.ceil(jobs.length / itemsPerPage);
  const paginatedJobs = jobs.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  // Generate array of page numbers
  const getPageNumbers = () => {
    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  };

  return (
    <ListContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Title>
        Job Postings 
        <JobCount>{jobs.length} total</JobCount>
      </Title>
      
      {error && <Error>{error}</Error>}
      
      {loading ? (
        <Loader>
          <i className="fas fa-spinner"></i>
          <p>Loading job postings...</p>
        </Loader>
      ) : paginatedJobs.length === 0 ? (
        <EmptyState>
          <i className="fas fa-briefcase" style={{ fontSize: '3rem', marginBottom: '1rem' }}></i>
          <p>No job postings found. Create a job posting to get started!</p>
        </EmptyState>
      ) : (
        <>
          <AnimatePresence>
            {paginatedJobs.map((job) => (
              <JobItem
                key={job.id}
                onClick={() => handleJobClick(job)}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <JobInfo>
                  <JobTitle>{job.title}</JobTitle>
                  <JobDetail>
                    <div>
                      <i className="fas fa-building"></i> {job.company}
                    </div>
                    <div>
                      <i className="fas fa-map-marker-alt"></i> {job.location || 'No location specified'}
                    </div>
                    <div>
                      <i className="fas fa-clock"></i> {job.job_type || 'Full-time'}
                    </div>
                    {job.experience_required && (
                      <div>
                        <i className="fas fa-briefcase"></i> {job.experience_required}+ years
                      </div>
                    )}
                  </JobDetail>
                  {job.skills_required && job.skills_required.length > 0 && (
                    <SkillTags>
                      {job.skills_required.slice(0, 5).map((skill, index) => (
                        <SkillTag key={index}>{skill}</SkillTag>
                      ))}
                      {job.skills_required.length > 5 && (
                        <SkillTag>+{job.skills_required.length - 5} more</SkillTag>
                      )}
                    </SkillTags>
                  )}
                </JobInfo>
                <ActionButtons>
                  <ActionButton 
                    color={props => props.theme.colors.error}
                    onClick={(e) => handleDeleteJob(job.id, e)}
                  >
                    <i className="fas fa-trash"></i>
                  </ActionButton>
                </ActionButtons>
              </JobItem>
            ))}
          </AnimatePresence>
          
          {totalPages > 1 && (
            <Pagination>
              <PaginationButton 
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
              >
                <i className="fas fa-chevron-left"></i>
              </PaginationButton>
              
              {getPageNumbers().map(page => (
                <PaginationButton 
                  key={page}
                  active={page === currentPage}
                  onClick={() => handlePageChange(page)}
                >
                  {page}
                </PaginationButton>
              ))}
              
              <PaginationButton 
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                <i className="fas fa-chevron-right"></i>
              </PaginationButton>
            </Pagination>
          )}
        </>
      )}
    </ListContainer>
  );
};

export default JobList;