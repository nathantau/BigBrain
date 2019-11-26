-- CREATE DATABASE bigbrain;
\c bigbrain
CREATE TABLE users(email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, salt VARCHAR(255) NOT NULL);
INSERT INTO users(email, password, salt) VALUES ('rando', 'rando', 'rando');
SELECT * FROM users;