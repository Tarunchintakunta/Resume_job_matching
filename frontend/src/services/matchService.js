import api from './api';

export const calculateMatches = async (jobId, resumeIds = null) => {
  try {
    const response = await api.post('/matches/calculate', {
      job_id: jobId,
      resume_ids: resumeIds
    });
    return response.data;
  } catch (error) {
    console.error('Error calculating matches:', error);
    throw error;
  }
};

export const getMatchesForJob = async (jobId) => {
  try {
    const response = await api.get(`/matches/job/${jobId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching matches for job ${jobId}:`, error);
    throw error;
  }
};

export const getMatchesForResume = async (resumeId) => {
  try {
    const response = await api.get(`/matches/resume/${resumeId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching matches for resume ${resumeId}:`, error);
    throw error;
  }
};