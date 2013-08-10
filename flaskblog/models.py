from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from flaskblog import app
from config import WHOOSH_ENABLED
from math import ceil

db = SQLAlchemy(app)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    userd = db.Column(db.String(100))

    def __init__(self, user):
        self.user = user

    def __repr__(self):
        return "<User: %s>" % (self.userd)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

tags = db.Table('posts_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)


class Post(db.Model):
   __tablename__ = 'posts'
   __searchable__ = ['text']

   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(120))
   text = db.Column(db.Text,)
   tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

   def __init__(self, title, text, tags):
        self.title = title
        self.text = text
        self.tags = tags
    
   def __repr__(self):
        return '<Title %r, Text %r, Tag %r>' %(self.title, self.text, self.tags)      


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(120))

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return '<Tag %r>' % self.tag


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
                num > self.pages - right_edge:
                
                if last + 1 != num:
                    yield None
                yield num
                last = num

if WHOOSH_ENABLED:
    import flask.ext.whooshalchemy as whooshalchemy
    whooshalchemy.whoosh_index(app, Post)