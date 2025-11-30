
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create recipes table
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    ingredients TEXT,
    instructions TEXT,
    cooking_time INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Create ratings table
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE(user_id, recipe_id)
);

-- Create indexes for better performance
CREATE INDEX idx_recipes_user_id ON recipes(user_id);
CREATE INDEX idx_recipes_title ON recipes(title);
CREATE INDEX idx_ratings_user_id ON ratings(user_id);
CREATE INDEX idx_ratings_recipe_id ON ratings(recipe_id);

-- Insert sample data (optional)
INSERT INTO users (username, email, hashed_password) VALUES 
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq9w5KS'),
('chef', 'chef@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq9w5KS');

INSERT INTO recipes (title, description, ingredients, instructions, cooking_time, user_id) VALUES 
('Spaghetti Carbonara', 'Classic Italian pasta dish', 'Pasta, Eggs, Bacon, Parmesan, Black Pepper', '1. Cook pasta 2. Fry bacon 3. Mix eggs and cheese 4. Combine all ingredients', 20, 1),
('Chicken Curry', 'Spicy Indian curry', 'Chicken, Onions, Garlic, Ginger, Curry Powder, Coconut Milk', '1. Marinate chicken 2. Sauté onions 3. Add spices 4. Simmer with coconut milk', 45, 2);

INSERT INTO ratings (rating, comment, user_id, recipe_id) VALUES 
(5, 'Amazing recipe! Very authentic.', 2, 1),
(4, 'Good but needs more spice.', 1, 2);