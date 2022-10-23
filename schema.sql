
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);

CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    username TEXT UNIQUE,
    active BOOLEAN
);

CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    companyname TEXT, 
    visible BOOLEAN
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies,
    companyname TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    posted_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE alikes (
    post_id SERIAL PRIMARY KEY,
    likes INTEGER,
    nonlikes INTEGER
);



