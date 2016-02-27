from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string

# Initialise the flask application
app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///thegoodybasket.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

import thegoodybasket.views
import thegoodybasket.signin
import thegoodybasket.endpoints

# Generate a random string token for CSRF protection on selected POST views.
def generate_csrf_token():
    if '_csrf_token' not in login_session:
        csrf_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
        login_session['_csrf_token'] = csrf_token
    return login_session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token
