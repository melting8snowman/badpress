
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    username TEXT UNIQUE,
    active BOOLEAN
);

CREATE TABLE alikes (
    post_id SERIAL PRIMARY KEY,
    likes INTEGER,
    nonlikes INTEGER
);

ALTER TABLE users DROP COLUMN is_admin;

INSERT INTO alikes (likes, nonlikes) select likes, 0 from posts order by id;

ALTER TABLE posts DROP COLUMN likes;