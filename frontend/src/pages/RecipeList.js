import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { recipeService } from '../services/api';

export const RecipeList = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const data = await recipeService.getRecipes();
        setRecipes(data);
      } catch (error) {
        console.error('Error fetching recipes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '2rem' }}>Loading recipes...</div>;
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Recipes</h1>
      {recipes.length === 0 ? (
        <p>No recipes found.</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
          {recipes.map(recipe => (
            <div key={recipe.id} style={{ border: '1px solid #dee2e6', borderRadius: '8px', padding: '1rem' }}>
              <h3>{recipe.title}</h3>
              <p>{recipe.description}</p>
              <p><strong>Cooking Time:</strong> {recipe.cooking_time} minutes</p>
              <Link to={`/recipes/${recipe.id}`} style={{ color: '#007bff', textDecoration: 'none' }}>
                View Details
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};