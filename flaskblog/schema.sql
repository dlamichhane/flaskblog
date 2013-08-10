DROP TABLE if exists admin, posts, tags, posts_tags;

CREATE TABLE admin (
	id SERIAL PRIMARY KEY,
	userd VARCHAR(100)
);

INSERT INTO admin (userd) VALUES ('admin');

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(120) NOT NULL,
  text TEXT NOT NULL
);

CREATE TABLE tags (
	id SERIAL PRIMARY KEY,
	tag VARCHAR(100)
);

CREATE TABLE posts_tags (
	post_id INTEGER references posts (id) ON UPDATE CASCADE ON DELETE CASCADE,
	tag_id INTEGER references tags(id) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT posts_tags_pkey PRIMARY KEY (post_id,tag_id)
);
