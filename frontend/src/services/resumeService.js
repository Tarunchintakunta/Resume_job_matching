import api from './api';
import { deleteResume, getResumeById, getResumes, uploadResume } from './api';

// Re-export the functions for backward compatibility
export { deleteResume, getResumeById, getResumes, uploadResume };

// For any additional resume-specific functions
export const searchResumes = async (query) => {
  try {
    const allResumes = await getResumes();
    // Simple search implementation
    return allResumes.filter(resume => 
      resume.name?.toLowerCase().includes(query.toLowerCase()) ||
      resume.skills?.some(skill => skill.toLowerCase().includes(query.toLowerCase())) ||
      resume.raw_text?.toLowerCase().includes(query.toLowerCase())
    );
  } catch (error) {
    console.error('Error searching resumes:', error);
    throw error;
  }
};

export default {
  deleteResume,
  getResumeById,
  getResumes,
  uploadResume,
  searchResumes
};