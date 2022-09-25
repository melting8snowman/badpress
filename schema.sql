
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    companyname TEXT
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    companyname TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    posted_at TIMESTAMP
);