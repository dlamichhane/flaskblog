== Welcome to flaskblog

 - pip install flask-sqlalchemy

- pip instal postgresql
- pip install sqlalchemy
- pip install flask
- pip install psycopg2
- pip install flask-login

If problem on installing psycopg2, install first
	sudo apt-get build-dep python-psycopg2
	sudo apt-get install libpq-dev
and
run the below command on the virutal environment

- pip install psycopg2

- pip install flask-wtf
- pip install Flask-WhooshAlchemy

== Not used
- pip sqlalchemy-migrate



== DATABASE FILE
Use Postgres database

== Use below text hint to create the database

postgresql://scott:tiger@localhost/flaskblog

```ruby
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
```