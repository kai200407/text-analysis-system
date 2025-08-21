import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from 'antd';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import DashboardContent from './components/DashboardContent';
import SentimentAnalysis from './components/SentimentAnalysis';
import KeywordExtraction from './components/KeywordExtraction';
import SummaryGeneration from './components/SummaryGeneration';
import SimilarityCalculation from './components/SimilarityCalculation';
import History from './components/History';
import Stats from './components/Stats';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

const { Content } = Layout;

function App() {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Content>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }>
              <Route index element={<DashboardContent />} />
              <Route path="sentiment" element={<SentimentAnalysis />} />
              <Route path="keywords" element={<KeywordExtraction />} />
              <Route path="summary" element={<SummaryGeneration />} />
              <Route path="similarity" element={<SimilarityCalculation />} />
              <Route path="history" element={<History />} />
              <Route path="stats" element={<Stats />} />
            </Route>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Content>
      </Layout>
    </Router>
  );
}

export default App; 