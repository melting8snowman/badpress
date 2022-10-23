ALTER TABLE users 
ADD is_admin BOOLEAN NOT NULL 
DEFAULT FALSE;

ALTER TABLE posts
ADD visible BOOLEAN NOT NULL
DEFAULT TRUE;

ALTER TABLE companies
ADD visible BOOLEAN NOT NULL
DEFAULT TRUE;

ALTER TABLE posts
ADD likes INTEGER NOT NULL
DEFAULT 0;

ALTER TABLE users DROP COLUMN is_admin;

INSERT INTO alikes (likes, nonlikes) select likes, 0 from posts order by id;

ALTER TABLE posts DROP COLUMN likes;