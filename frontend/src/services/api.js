import axios from 'axios';

// All requests go through Ingress
const API_BASE_URL = "/api/users";
const RECIPE_BASE_URL = "/api/recipes";
const RATING_BASE_URL = "/api/ratings";

// User/Auth API -----------------------------

const api = axios.create({
  baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const response = await api.post("/token", formData);
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post("/register", userData);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get("/users/me");
    return response.data;
  }
};


// Recipe API --------------------------------

export const recipeService = {

  getRecipes: async () => {
    const res = await axios.get(`${RECIPE_BASE_URL}`);
    return res.data;
  },

  getRecipe: async (id) => {
    const res = await axios.get(`${RECIPE_BASE_URL}/${id}`);
    return res.data;
  },

  createRecipe: async (recipeData) => {
    const token = localStorage.getItem("token");
    const res = await axios.post(`${RECIPE_BASE_URL}`, recipeData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
  },

  updateRecipe: async (id, recipeData) => {
    const token = localStorage.getItem("token");
    const res = await axios.put(`${RECIPE_BASE_URL}/${id}`, recipeData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
  },

  deleteRecipe: async (id) => {
    const token = localStorage.getItem("token");
    const res = await axios.delete(`${RECIPE_BASE_URL}/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
  }
};


// Rating API --------------------------------

export const ratingService = {

  getRecipeRatings: async (recipeId) => {
    const res = await axios.get(`${RATING_BASE_URL}/recipes/${recipeId}/ratings`);
    return res.data;
  },

  createRating: async (ratingData) => {
    const token = localStorage.getItem("token");
    const res = await axios.post(`${RATING_BASE_URL}/ratings`, ratingData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
  },

  updateRating: async (id, ratingData) => {
    const token = localStorage.getItem("token");
    const res = await axios.put(`${RATING_BASE_URL}/ratings/${id}`, ratingData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
  },

  deleteRating: async (id) => {
    const token = localStorage.getItem("token");
    const res = await axios.delete(`${RATING_BASE_URL}/ratings/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
  }
};
