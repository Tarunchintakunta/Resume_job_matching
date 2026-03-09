import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const CalcContainer = styled(motion.div)`
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
`;

const CalcTitle = styled.h2`
  font-size: 1.25rem;
  color: #212529;
  margin-bottom: 16px;
`;

const FormRow = styled.div`
  display: flex;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
`;

const FormGroup = styled.div`
  flex: 1;
  min-width: 200px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 0.9rem;
  color: #495057;
`;

const Select = styled.select`
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s;

  &:focus {
    border-color: #4361ee;
    outline: none;
    box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15);
  }
`;

const CalculateButton = styled.button`
  padding: 10px 28px;
  background: linear-gradient(90deg, #4361ee, #4895ef);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const MatchCalculation = ({ jobs = [], selectedJobId, onJobChange, onCalculate, loading }) => {
  return (
    <CalcContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <CalcTitle>Calculate Matches</CalcTitle>
      <FormRow>
        <FormGroup>
          <Label htmlFor="job-select">Select Job Posting</Label>
          <Select
            id="job-select"
            value={selectedJobId || ''}
            onChange={(e) => onJobChange(e.target.value)}
          >
            <option value="">-- Select a job posting --</option>
            {jobs.map((job) => (
              <option key={job.id} value={job.id}>
                {job.title} at {job.company}
              </option>
            ))}
          </Select>
        </FormGroup>
        <CalculateButton
          onClick={onCalculate}
          disabled={!selectedJobId || loading}
        >
          {loading ? 'Calculating...' : 'Calculate Matches'}
        </CalculateButton>
      </FormRow>
    </CalcContainer>
  );
};

export default MatchCalculation;
