CREATE DATABASE dhuite202003585db;

USE dhuite202003585db;

# Create 'dhuite202003585users' table
CREATE TABLE IF NOT EXISTS dhuite202003585users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

# Insert default user
INSERT INTO dhuite202003585users (username, password) VALUES ('default', 'default');
