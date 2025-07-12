import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import GlobalStyles from './styles/GlobalStyles';
import theme from './styles/theme';

// Pages
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import ResumesPage from './pages/ResumesPage';
import JobsPage from './pages/JobsPage';
import MatchesPage from './pages/MatchesPage';

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/resumes" element={<ResumesPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/matches" element={<MatchesPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;