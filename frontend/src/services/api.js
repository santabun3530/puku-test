import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';
const RECIPE_SERVICE_URL = process.env.REACT_APP_RECIPE_SERVICE_URL || 'http://localhost:8002';
const RATING_SERVICE_URL = process.env.REACT_APP_RATING_SERVICE_URL || 'http://localhost:8003';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export const authService = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/token', formData);
    return response.data;
  },
  
  register: async (userData) => {
    const response = await api.post('/register', userData);
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  }
};

export const recipeService = {
  getRecipes: async () => {
    const response = await axios.get(`${RECIPE_SERVICE_URL}/recipes`);
    return response.data;
  },
  
  getRecipe: async (id) => {
    const response = await axios.get(`${RECIPE_SERVICE_URL}/recipes/${id}`);
    return response.data;
  },
  
  createRecipe: async (recipeData) => {
    const token = localStorage.getItem('token');
    const response = await axios.post(`${RECIPE_SERVICE_URL}/recipes`, recipeData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },
  
  updateRecipe: async (id, recipeData) => {
    const token = localStorage.getItem('token');
    const response = await axios.put(`${RECIPE_SERVICE_URL}/recipes/${id}`, recipeData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },
  
  deleteRecipe: async (id) => {
    const token = localStorage.getItem('token');
    const response = await axios.delete(`${RECIPE_SERVICE_URL}/recipes/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  }
};

export const ratingService = {
  getRecipeRatings: async (recipeId) => {
    const response = await axios.get(`${RATING_SERVICE_URL}/recipes/${recipeId}/ratings`);
    return response.data;
  },
  
  createRating: async (ratingData) => {
    const token = localStorage.getItem('token');
    const response = await axios.post(`${RATING_SERVICE_URL}/ratings`, ratingData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },
  
  updateRating: async (id, ratingData) => {
    const token = localStorage.getItem('token');
    const response = await axios.put(`${RATING_SERVICE_URL}/ratings/${id}`, ratingData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },
  
  deleteRating: async (id) => {
    const token = localStorage.getItem('token');
    const response = await axios.delete(`${RATING_SERVICE_URL}/ratings/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  }
};