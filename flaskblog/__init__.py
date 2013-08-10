#imports
from flask import Flask
from flask.ext.login import LoginManager, UserMixin
from helper import url_for_other_page
import os

basedir = os.path.abspath(os.path.dirname(__file__))

#Application creation
app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://scott:tiger@localhost/flaskblog'
app.config['WHOOSH_BASE'] = os.path.join(basedir, 'search.db')
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

from models import db
db.app = app
db.init_app(app)
from flaskblog import views, models