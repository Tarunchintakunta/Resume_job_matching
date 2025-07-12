import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { createJob } from '../../services/jobService';
import Button from '../common/Button';

const FormContainer = styled(motion.div)`
  background-color: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.borderRadius.medium};
  padding: ${props => props.theme.spacing.xl};
  box-shadow: ${props => props.theme.shadows.medium};
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const Title = styled.h2`
  font-size: ${props => props.theme.fontSizes.large};
  margin-bottom: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.text};
`;

const FormGroup = styled.div`
  margin-bottom: ${props => props.theme.spacing.md};
`;

const Label = styled.label`
  display: block;
  margin-bottom: ${props => props.theme.spacing.sm};
  font-weight: 500;
  color: ${props => props.theme.colors.text};
`;

const Input = styled.input`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: ${props => props.theme.fontSizes.regular};
  transition: border-color ${props => props.theme.transitions.fast};
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
    outline: none;
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: ${props => props.theme.fontSizes.regular};
  transition: border-color ${props => props.theme.transitions.fast};
  min-height: 120px;
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
    outline: none;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: ${props => props.theme.spacing.sm};
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: ${props => props.theme.borderRadius.small};
  font-size: ${props => props.theme.fontSizes.regular};
  transition: border-color ${props => props.theme.transitions.fast};
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
    outline: none;
  }
`;

const TagInput = styled.div`
  display: flex;
  flex-wrap: wrap;
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: ${props => props.theme.borderRadius.small};
  padding: ${props => props.theme.spacing.xs};
  
  &:focus-within {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const Tag = styled.div`
  display: inline-flex;
  align-items: center;
  background-color: ${props => props.theme.colors.primary};
  color: white;
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: ${props => props.theme.borderRadius.small};
  margin: ${props => props.theme.spacing.xs};
  font-size: ${props => props.theme.fontSizes.small};
`;

const TagRemove = styled.button`
  background: none;
  border: none;
  color: white;
  margin-left: ${props => props.theme.spacing.xs};
  cursor: pointer;
  font-size: ${props => props.theme.fontSizes.small};
`;

const TagInputField = styled.input`
  flex: 1;
  border: none;
  outline: none;
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  font-size: ${props => props.theme.fontSizes.regular};
  min-width: 120px;
`;

const ButtonContainer = styled.div`
  margin-top: ${props => props.theme.spacing.lg};
  display: flex;
  justify-content: flex-end;
  gap: ${props => props.theme.spacing.md};
`;

const Alert = styled.div`
  padding: ${props => props.theme.spacing.md};
  margin: ${props => props.theme.spacing.md} 0;
  border-radius: ${props => props.theme.borderRadius.small};
  color: white;
  background-color: ${props => props.type === 'success' 
    ? props.theme.colors.success 
    : props.theme.colors.error};
`;

const TwoColumnLayout = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
  }
`;

const JobCreate = ({ onJobCreated }) => {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    description: '',
    requirements: [],
    qualifications: [],
    skills_required: [],
    experience_required: 0,
    location: '',
    job_type: 'Full-time',
    salary_range: ''
  });
  
  const [currentRequirement, setCurrentRequirement] = useState('');
  const [currentQualification, setCurrentQualification] = useState('');
  const [currentSkill, setCurrentSkill] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleAddRequirement = (e) => {
    e.preventDefault();
    if (currentRequirement.trim()) {
      setFormData({
        ...formData,
        requirements: [...formData.requirements, currentRequirement.trim()]
      });
      setCurrentRequirement('');
    }
  };

  const handleRemoveRequirement = (index) => {
    const newRequirements = [...formData.requirements];
    newRequirements.splice(index, 1);
    setFormData({
      ...formData,
      requirements: newRequirements
    });
  };

  const handleAddQualification = (e) => {
    e.preventDefault();
    if (currentQualification.trim()) {
      setFormData({
        ...formData,
        qualifications: [...formData.qualifications, currentQualification.trim()]
      });
      setCurrentQualification('');
    }
  };

  const handleRemoveQualification = (index) => {
    const newQualifications = [...formData.qualifications];
    newQualifications.splice(index, 1);
    setFormData({
      ...formData,
      qualifications: newQualifications
    });
  };

  const handleAddSkill = (e) => {
    e.preventDefault();
    if (currentSkill.trim()) {
      setFormData({
        ...formData,
        skills_required: [...formData.skills_required, currentSkill.trim()]
      });
      setCurrentSkill('');
    }
  };

  const handleRemoveSkill = (index) => {
    const newSkills = [...formData.skills_required];
    newSkills.splice(index, 1);
    setFormData({
      ...formData,
      skills_required: newSkills
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title || !formData.company || !formData.description) {
      setAlert({
        type: 'error',
        message: 'Please fill in all required fields (title, company, description).'
      });
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await createJob(formData);
      setAlert({
        type: 'success',
        message: 'Job posting created successfully!'
      });
      
      // Reset form
      setFormData({
        title: '',
        company: '',
        description: '',
        requirements: [],
        qualifications: [],
        skills_required: [],
        experience_required: 0,
        location: '',
        job_type: 'Full-time',
        salary_range: ''
      });
      
      if (onJobCreated) {
        onJobCreated(response);
      }
    } catch (error) {
      setAlert({
        type: 'error',
        message: error.response?.data?.detail || 'Error creating job posting. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      title: '',
      company: '',
      description: '',
      requirements: [],
      qualifications: [],
      skills_required: [],
      experience_required: 0,
      location: '',
      job_type: 'Full-time',
      salary_range: ''
    });
    setAlert(null);
  };

  return (
    <FormContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Title>Create Job Posting</Title>
      
      {alert && (
        <Alert type={alert.type}>
          {alert.message}
        </Alert>
      )}
      
      <form onSubmit={handleSubmit}>
        <TwoColumnLayout>
          <FormGroup>
            <Label htmlFor="title">Job Title *</Label>
            <Input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="e.g. Software Engineer"
              required
            />
          </FormGroup>
          
          <FormGroup>
            <Label htmlFor="company">Company *</Label>
            <Input
              type="text"
              id="company"
              name="company"
              value={formData.company}
              onChange={handleChange}
              placeholder="e.g. Acme Inc."
              required
            />
          </FormGroup>
        </TwoColumnLayout>
        
        <FormGroup>
          <Label htmlFor="description">Job Description *</Label>
          <TextArea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe the role, responsibilities, and your ideal candidate"
            required
          />
        </FormGroup>
        
        <TwoColumnLayout>
          <FormGroup>
            <Label htmlFor="location">Location</Label>
            <Input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g. New York, NY or Remote"
            />
          </FormGroup>
          
          <FormGroup>
            <Label htmlFor="job_type">Job Type</Label>
            <Select
              id="job_type"
              name="job_type"
              value={formData.job_type}
              onChange={handleChange}
            >
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Freelance">Freelance</option>
              <option value="Internship">Internship</option>
              <option value="Remote">Remote</option>
            </Select>
          </FormGroup>
        </TwoColumnLayout>
        
        <TwoColumnLayout>
          <FormGroup>
            <Label htmlFor="experience_required">Years of Experience Required</Label>
            <Input
              type="number"
              id="experience_required"
              name="experience_required"
              value={formData.experience_required}
              onChange={handleChange}
              min="0"
              max="20"
            />
          </FormGroup>
          
          <FormGroup>
            <Label htmlFor="salary_range">Salary Range</Label>
            <Input
              type="text"
              id="salary_range"
              name="salary_range"
              value={formData.salary_range}
              onChange={handleChange}
              placeholder="e.g. $50,000 - $70,000"
            />
          </FormGroup>
        </TwoColumnLayout>
        
        <FormGroup>
          <Label>Required Skills</Label>
          <TagInput>
            {formData.skills_required.map((skill, index) => (
              <Tag key={index}>
                {skill}
                <TagRemove type="button" onClick={() => handleRemoveSkill(index)}>×</TagRemove>
              </Tag>
            ))}
            <TagInputField
              type="text"
              value={currentSkill}
              onChange={(e) => setCurrentSkill(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddSkill(e)}
              placeholder="Add skills..."
            />
          </TagInput>
        </FormGroup>
        
        <FormGroup>
          <Label>Job Requirements</Label>
          <TagInput>
            {formData.requirements.map((req, index) => (
              <Tag key={index}>
                {req}
                <TagRemove type="button" onClick={() => handleRemoveRequirement(index)}>×</TagRemove>
              </Tag>
            ))}
            <TagInputField
              type="text"
              value={currentRequirement}
              onChange={(e) => setCurrentRequirement(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddRequirement(e)}
              placeholder="Add requirements..."
            />
          </TagInput>
        </FormGroup>
        
        <FormGroup>
          <Label>Preferred Qualifications</Label>
          <TagInput>
            {formData.qualifications.map((qual, index) => (
              <Tag key={index}>
                {qual}
                <TagRemove type="button" onClick={() => handleRemoveQualification(index)}>×</TagRemove>
              </Tag>
            ))}
            <TagInputField
              type="text"
              value={currentQualification}
              onChange={(e) => setCurrentQualification(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAddQualification(e)}
              placeholder="Add qualifications..."
            />
          </TagInput>
        </FormGroup>
        
        <ButtonContainer>
          <Button type="button" variant="outlined" onClick={handleReset}>
            Reset
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Job'}
          </Button>
        </ButtonContainer>
      </form>
    </FormContainer>
  );
};

export default JobCreate;