import api from './api';

export const getResumes = async () => {
  try {
    const response = await api.get('/resumes');
    return response.data;
  } catch (error) {
    console.error('Error fetching resumes:', error);
    throw error;
  }
};

export const getResumeById = async (id) => {
  try {
    const response = await api.get(`/resumes/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching resume with id ${id}:`, error);
    throw error;
  }
};

export const uploadResume = async (formData) => {
  try {
    const response = await api.post('/resumes', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading resume:', error);
    throw error;
  }
};

export const deleteResume = async (id) => {
  try {
    const response = await api.delete(`/resumes/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting resume with id ${id}:`, error);
    throw error;
  }
};