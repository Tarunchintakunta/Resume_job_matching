import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { uploadResume } from '../../services/resumeService';
import Button from '../common/Button';

const UploadContainer = styled(motion.div)`
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

const FileInput = styled.input`
  display: none;
`;

const FileInputLabel = styled.label`
  display: block;
  width: 100%;
  padding: ${props => props.theme.spacing.lg};
  border: 2px dashed ${props => props.theme.colors.primary};
  border-radius: ${props => props.theme.borderRadius.medium};
  text-align: center;
  cursor: pointer;
  transition: all ${props => props.theme.transitions.fast};
  background-color: rgba(67, 97, 238, 0.05);
  
  &:hover {
    background-color: rgba(67, 97, 238, 0.1);
  }
`;

const FileName = styled.div`
  margin-top: ${props => props.theme.spacing.sm};
  font-size: ${props => props.theme.fontSizes.small};
  color: ${props => props.theme.colors.lightText};
`;

const UploadIcon = styled.div`
  font-size: 2rem;
  color: ${props => props.theme.colors.primary};
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const UploadText = styled.div`
  font-weight: 500;
  margin-bottom: ${props => props.theme.spacing.xs};
`;

const UploadSubtext = styled.div`
  font-size: ${props => props.theme.fontSizes.small};
  color: ${props => props.theme.colors.lightText};
`;

const ButtonContainer = styled.div`
  margin-top: ${props => props.theme.spacing.lg};
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

const ResumeUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setAlert({
        type: 'error',
        message: 'Please select a file to upload.'
      });
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    setLoading(true);
    
    try {
      console.log('Uploading file:', file.name);
      const response = await uploadResume(formData);
      console.log('Upload response:', response);
      
      setAlert({
        type: 'success',
        message: 'Resume uploaded successfully!'
      });
      setFile(null);
      if (onUploadSuccess) {
        onUploadSuccess(response);
      }
    } catch (error) {
      console.error('Error in upload component:', error);
      setAlert({
        type: 'error',
        message: error.response?.data?.detail || 'Error uploading resume. Please try again.'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <UploadContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Title>Upload Resume</Title>
      
      {alert && (
        <Alert type={alert.type}>
          {alert.message}
        </Alert>
      )}
      
      <form onSubmit={handleSubmit}>
        <FormGroup>
          <Label htmlFor="resume-file">Resume File</Label>
          <FileInput 
            type="file" 
            id="resume-file" 
            accept=".pdf,.json" 
            onChange={handleFileChange} 
          />
          <FileInputLabel htmlFor="resume-file">
            <UploadIcon>
              <i className="fas fa-file-upload"></i>
            </UploadIcon>
            <UploadText>Drag & drop a file here, or click to browse</UploadText>
            <UploadSubtext>Supports PDF and JSON files up to 10MB</UploadSubtext>
            {file && <FileName>Selected file: {file.name}</FileName>}
          </FileInputLabel>
        </FormGroup>
        
        <ButtonContainer>
          <Button type="submit" disabled={loading}>
            {loading ? 'Uploading...' : 'Upload Resume'}
          </Button>
        </ButtonContainer>
      </form>
    </UploadContainer>
  );
};

export default ResumeUpload;