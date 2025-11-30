import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { recipeService, ratingService } from '../services/api';

export const RecipeDetail = () => {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [ratings, setRatings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newRating, setNewRating] = useState({ rating: 5, comment: '' });
  const [userRatings, setUserRatings] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const recipeData = await recipeService.getRecipe(id);
        setRecipe(recipeData);
        
        const ratingsData = await ratingService.getRecipeRatings(id);
        setRatings(ratingsData);
        
        // Create a map of user's ratings for easy management
        const userRatingMap = {};
        ratingsData.forEach(rating => {
          userRatingMap[rating.id] = rating;
        });
        setUserRatings(userRatingMap);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleRatingSubmit = async (e) => {
    e.preventDefault();
    try {
      await ratingService.createRating({ ...newRating, recipe_id: parseInt(id) });
      const ratingsData = await ratingService.getRecipeRatings(id);
      setRatings(ratingsData);
      setNewRating({ rating: 5, comment: '' });
    } catch (error) {
      console.error('Error creating rating:', error);
    }
  };

  const handleDeleteRating = async (ratingId) => {
    try {
      await ratingService.deleteRating(ratingId);
      const ratingsData = await ratingService.getRecipeRatings(id);
      setRatings(ratingsData);
    } catch (error) {
      console.error('Error deleting rating:', error);
    }
  };

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '2rem' }}>Loading...</div>;
  }

  if (!recipe) {
    return <div style={{ textAlign: 'center', padding: '2rem' }}>Recipe not found</div>;
  }

  const token = localStorage.getItem('token');

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>{recipe.title}</h1>
        {token && (
          <Link 
            to={`/update-recipe/${id}`} 
            style={{ 
              padding: '0.5rem 1rem', 
              backgroundColor: '#28a745', 
              color: 'white', 
              textDecoration: 'none', 
              borderRadius: '4px' 
            }}
          >
            Edit Recipe
          </Link>
        )}
      </div>
      <p><strong>Description:</strong> {recipe.description}</p>
      <p><strong>Cooking Time:</strong> {recipe.cooking_time} minutes</p>
      
      <div style={{ marginTop: '2rem' }}>
        <h3>Ingredients</h3>
        <p style={{ whiteSpace: 'pre-line' }}>{recipe.ingredients}</p>
      </div>
      
      <div style={{ marginTop: '2rem' }}>
        <h3>Instructions</h3>
        <p style={{ whiteSpace: 'pre-line' }}>{recipe.instructions}</p>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h3>Ratings & Reviews</h3>
        {ratings.length === 0 ? (
          <p>No ratings yet.</p>
        ) : (
          ratings.map(rating => (
            <div key={rating.id} style={{ border: '1px solid #dee2e6', borderRadius: '4px', padding: '1rem', marginBottom: '1rem', position: 'relative' }}>
              <p><strong>Rating:</strong> {rating.rating}/5</p>
              <p>{rating.comment}</p>
              {token && (
                <button 
                  onClick={() => handleDeleteRating(rating.id)}
                  style={{ 
                    position: 'absolute', 
                    top: '0.5rem', 
                    right: '0.5rem', 
                    backgroundColor: '#dc3545', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px', 
                    padding: '0.25rem 0.5rem',
                    cursor: 'pointer'
                  }}
                >
                  Delete
                </button>
              )}
            </div>
          ))
        )}
      </div>

      {token && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Add Your Rating</h3>
          <form onSubmit={handleRatingSubmit}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Rating:</label>
              <select
                value={newRating.rating}
                onChange={(e) => setNewRating({ ...newRating, rating: parseInt(e.target.value) })}
                style={{ padding: '0.5rem', border: '1px solid #ced4da', borderRadius: '4px' }}
              >
                <option value={1}>1</option>
                <option value={2}>2</option>
                <option value={3}>3</option>
                <option value={4}>4</option>
                <option value={5}>5</option>
              </select>
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Comment:</label>
              <textarea
                value={newRating.comment}
                onChange={(e) => setNewRating({ ...newRating, comment: e.target.value })}
                required
                style={{ width: '100%', padding: '0.5rem', border: '1px solid #ced4da', borderRadius: '4px', minHeight: '100px' }}
              />
            </div>
            <button type="submit" style={{ padding: '0.5rem 1rem', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
              Submit Rating
            </button>
          </form>
        </div>
      )}
    </div>
  );
};