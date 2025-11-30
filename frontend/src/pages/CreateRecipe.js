import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { recipeService } from '../services/api';

export const CreateRecipe = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    ingredients: '',
    instructions: '',
    cooking_time: 30
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.name === 'cooking_time' ? parseInt(e.target.value) : e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await recipeService.createRecipe(formData);
      navigate('/');
    } catch (err) {
      setError('Failed to create recipe');
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '2rem auto', padding: '2rem', border: '1px solid #dee2e6', borderRadius: '8px' }}>
      <h2>Create Recipe</h2>
      {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Title:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '0.5rem', border: '1px solid #ced4da', borderRadius: '4px' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '0.5rem', border: '1px solid #ced4da', borderRadius: '4px', minHeight: '80px' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Ingredients:</label>
          <textarea
            name="ingredients"
            value={formData.ingredients}
            onChange={handleChange}
            required
            placeholder="Enter ingredients, one per line"
            style={{ width: '100%', padding: '0.5rem', border: '1px solid #ced4da', borderRadius: '4px', minHeight: '100px' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Instructions:</label>
          <textarea
            name="instructions"
            value={formData.instructions}
            onChange={handleChange}
            required
            placeholder="Enter cooking instructions"
            style={{ width: '100%', padding: '0.5rem', border: '1px solid #ced4da', borderRadius: '4px', minHeight: '150px' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Cooking Time (minutes):</label>
          <input
            type="number"
            name="cooking_time"
            value={formData.cooking_time}
            onChange={handleChange}
            required
            min="1"
            style={{ width: '100%', padding: '0.5rem', border: '1px solid #ced4da', borderRadius: '4px' }}
          />
        </div>
        <button type="submit" style={{ width: '100%', padding: '0.5rem', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}>
          Create Recipe
        </button>
      </form>
    </div>
  );
};