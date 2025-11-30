import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export const Navbar = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Listen for storage changes and authentication state
  useEffect(() => {
    const handleStorageChange = () => {
      setToken(localStorage.getItem('token'));
    };

    // Listen for storage events (from other tabs/windows)
    window.addEventListener('storage', handleStorageChange);
    
    // Custom event for login/logout within same tab
    window.addEventListener('authChange', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('authChange', handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    // Dispatch custom event to notify other components
    window.dispatchEvent(new Event('authChange'));
    window.location.href = '/';
  };

  return (
    <nav style={{ padding: '1rem', backgroundColor: '#f8f9fa', borderBottom: '1px solid #dee2e6' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ textDecoration: 'none', fontSize: '1.5rem', fontWeight: 'bold' }}>
          Recipe App
        </Link>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <Link to="/" style={{ textDecoration: 'none', color: '#007bff' }}>Home</Link>
          {token ? (
            <>
              <Link to="/create-recipe" style={{ textDecoration: 'none', color: '#007bff' }}>Create Recipe</Link>
              <button onClick={handleLogout} style={{ border: 'none', background: 'none', color: '#dc3545', cursor: 'pointer' }}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={{ textDecoration: 'none', color: '#007bff' }}>Login</Link>
              <Link to="/register" style={{ textDecoration: 'none', color: '#007bff' }}>Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};