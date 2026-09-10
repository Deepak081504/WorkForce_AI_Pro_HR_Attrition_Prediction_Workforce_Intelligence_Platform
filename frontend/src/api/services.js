import API from './axios';

export const authService = {
  login: async (credentials) => (await API.post('/auth/login', credentials)).data,
  getMe: async () => (await API.get('/auth/me')).data,
};

export const employeeService = {
  list: async () => (await API.get('/employees')).data,
  get: async (id) => (await API.get(`/employees/${id}`)).data,
  create: async (payload) => (await API.post('/employees', payload)).data,
  delete: async (id) => (await API.delete(`/employees/${id}`)).data,
};

export const predictionService = {
  predict: async (payload) => (await API.post('/predictions/attrition', payload)).data,
  getHighRisk: async () => (await API.get('/predictions/high-risk')).data,
  getAnalyticsDashboard: async () => (await API.get('/attrition-analytics/dashboard')).data,
};

export const attendanceService = {
  list: async () => (await API.get('/attendance')).data,
  create: async (payload) => (await API.post('/attendance', payload)).data,
  update: async (id, payload) => (await API.put(`/attendance/${id}`, payload)).data,
  getShifts: async () => (await API.get('/shifts')).data,
};

export const payrollService = {
  list: async () => (await API.get('/payroll')).data,
  create: async (payload) => (await API.post('/payroll', payload)).data,
};

export const analyticsService = {
  getOverview: async () => (await API.get('/analytics/overview')).data,
};

export const interventionService = {
  list: async () => (await API.get('/interventions')).data,
  create: async (payload) => (await API.post('/interventions', payload)).data,
  getAlerts: async () => (await API.get('/alerts')).data,
};

export const modelTrainingService = {
  triggerTraining: async (datasetId = 1) => (await API.post(`/ml/train/${datasetId}`)).data,
  getRecommendations: async () => {
    try {
      return (await API.get('/ai-recommendations')).data;
    } catch {
      return [];
    }
  },
};

export const datasetService = {
  list: async () => {
    const token = localStorage.getItem('token');
    const res = await API.get('/datasets', {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    return res.data;
  },
  upload: async (formData) => {
    const token = localStorage.getItem('token');
    const res = await API.post('/datasets', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
    return res.data;
  },
  delete: async (id) => (await API.delete(`/datasets/${id}`)).data,
};