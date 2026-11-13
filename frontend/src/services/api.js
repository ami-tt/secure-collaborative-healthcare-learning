import axios from 'axios';



const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';



const apiClient = axios.create({

  baseURL: API_BASE_URL,

  headers: {

    'Content-Type': 'application/json',

  },

});



// Request interceptor to attach JWT token

apiClient.interceptors.request.use(

  (config) => {

    const token = localStorage.getItem('fl_auth_token');

    if (token) {

      config.headers['Authorization'] = `Bearer ${token}`;

    }

    return config;

  },

  (error) => Promise.reject(error)

);



// Response interceptor to handle 401s

apiClient.interceptors.response.use(

  (response) => response,

  (error) => {

    if (error.response && error.response.status === 401) {

      // Clear token if expired or invalid

      localStorage.removeItem('fl_auth_token');

      localStorage.removeItem('fl_user_data');

    }

    return Promise.reject(error);

  }

);



export const authService = {

  login: async (email, password) => {

    const response = await apiClient.post('/auth/login', { email, password });

    if (response.data.access_token) {

      localStorage.setItem('fl_auth_token', response.data.access_token);

      localStorage.setItem('fl_user_data', JSON.stringify(response.data));

    }

    return response.data;

  },

  register: async (userData) => {

    const response = await apiClient.post('/auth/register', userData);

    return response.data;

  },

  getMe: async () => {

    const response = await apiClient.get('/auth/me');

    return response.data;

  },

  logout: () => {

    localStorage.removeItem('fl_auth_token');

    localStorage.removeItem('fl_user_data');

  },

  getCurrentUser: () => {

    const data = localStorage.getItem('fl_user_data');

    return data ? JSON.parse(data) : null;

  },

  getToken: () => localStorage.getItem('fl_auth_token'),

};



export const userService = {

  getUsers: async (role = null) => {

    const params = role ? { role } : {};

    const response = await apiClient.get('/users/', { params });

    return response.data;

  },

  updateUser: async (userId, updateData) => {

    const response = await apiClient.patch(`/users/${userId}`, updateData);

    return response.data;

  },

};



export const institutionService = {

  getInstitutions: async (status = null) => {

    const params = status ? { status_filter: status } : {};

    const response = await apiClient.get('/institutions/', { params });

    return response.data;

  },

  createInstitution: async (data) => {

    const response = await apiClient.post('/institutions/', data);

    return response.data;

  },

  updateStatus: async (id, newStatus) => {

    const response = await apiClient.patch(`/institutions/${id}/status?new_status=${newStatus}`);

    return response.data;

  },

};



export const datasetService = {

  getDatasets: async (institutionId = null) => {

    const params = institutionId ? { institution_id: institutionId } : {};

    const response = await apiClient.get('/datasets/', { params });

    return response.data;

  },

  createDataset: async (data) => {

    const response = await apiClient.post('/datasets/', data);

    return response.data;

  },

};



export const flService = {

  getProjects: async () => {

    const response = await apiClient.get('/fl/projects');

    return response.data;

  },

  createProject: async (data) => {

    const response = await apiClient.post('/fl/projects', data);

    return response.data;

  },

  getSessions: async (projectId = null) => {

    const params = projectId ? { project_id: projectId } : {};

    const response = await apiClient.get('/fl/sessions', { params });

    return response.data;

  },

  createSession: async (data) => {

    const response = await apiClient.post('/fl/sessions', data);

    return response.data;

  },

};



export const auditService = {

  getAuditLogs: async (limit = 50) => {

    const response = await apiClient.get(`/audit/?limit=${limit}`);

    return response.data;

  },

};



export const systemService = {

  getHealth: async () => {

    const response = await axios.get('http://localhost:8000/health');

    return response.data;

  },

};
// Cardiovascular Risk Prediction Service
export const predictionService = {
  predict: async (patientData) => {
    const response = await apiClient.post(
      '/predictions/predict',
      patientData
    );

    return response.data;
  },
};



export default apiClient;
