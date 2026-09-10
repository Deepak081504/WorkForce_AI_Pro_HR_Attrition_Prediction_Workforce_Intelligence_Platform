import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ProtectedRoute from './components/layout/ProtectedRoute';
import EnterpriseLayout from './components/layout/EnterpriseLayout';
import AttritionCockpit from './pages/attrition/AttritionCockpit';
import EmployeeList from './pages/employees/EmployeeList';
import WorkforceAnalytics from './pages/analytics/WorkforceAnalytics';
import AttendanceShifts from './pages/attendance/AttendanceShifts';
import PayrollEngine from './pages/payroll/PayrollEngine';
import RetentionInterventions from './pages/retention/RetentionInterventions';
import ModelTraining from './pages/models/ModelTraining';
import PerformanceHub from './pages/performance/PerformanceHub';
import RecruitmentPipeline from './pages/recruitment/RecruitmentPipeline';
import SystemSettings from './pages/settings/SystemSettings';
import LeaveManagement from './pages/leaves/LeaveManagement';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Authenticated Workspace */}
        <Route element={<ProtectedRoute />}>
          <Route element={<EnterpriseLayout />}>
            <Route path="/" element={<Navigate to="/attrition" replace />} />
            <Route path="/attrition" element={<AttritionCockpit />} />
            <Route path="/employees" element={<EmployeeList />} />
            <Route path="/analytics" element={<WorkforceAnalytics />} />
            <Route path="/attendance" element={<AttendanceShifts />} />
            <Route path="/payroll" element={<PayrollEngine />} />
            <Route path="/interventions" element={<RetentionInterventions />} />
            <Route path="/model-training" element={<ModelTraining />} />
            <Route path="/performance" element={<PerformanceHub />} />
            <Route path="/recruitment" element={<RecruitmentPipeline />} />
            <Route path="/settings" element={<SystemSettings />} />
            <Route path="/leaves" element={<LeaveManagement />} />
          </Route>
        </Route>

        {/* Catch-all fallback */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}