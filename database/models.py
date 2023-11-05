## Imports
import os
from dotenv import find_dotenv, dotenv_values
from sqlalchemy import Column, String, Integer, create_engine
from dotenv import find_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy
import json


## Loading environement variable
ENV_FILE = find_dotenv(raise_error_if_not_found = True)
if ENV_FILE:
    env = dotenv_values(ENV_FILE)

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


## Setup DB
db = SQLAlchemy()


## DB Function
# Check if the environment variables are set
def validate_db():
    if db_host is None:
        print("DB IP address and port are not set.")
        return False
    if db_user is None:
        print("DB user name is not set.")
        return False
    if db_password is None:
        print("DB user password is not set.")
        return False
    if db_name is None:
        print("Database name is not set.")
        return False
    return True

# Setup DB
def setup_db(app, database_name=db_name):
    if not validate_db():
        raise Exception("DB variable is not set!")

    database_path ="postgresql://{}:{}@{}/{}"\
        .format(db_host, db_user, db_password, database_name)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


## Define model
# Movies
class Movie(db.Model):
    __tablename__ = 'movies'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    casting_site = db.Column(db.String, nullable=True)
    revenue = db.Column(db.Integer, nullable=True)
    actor_ids = db.Column(db.ARRAY(db.Integer), nullable=True)


    def __init__(self, title, release_date, actor_ids=[], casting_site=None):
        self.title = title
        self.release_date = release_date
        self.actor_ids = actor_ids
        self.casting_site = casting_site

    # format to json - short info
    def format_short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    # format to json - more info
    def format_details(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'casting_site': self.casting_site,
            'revenue': self.revenue,
        }

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()
    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Actor
class Actor(db.Model):
    __tablename__ = 'actors'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    # insert
    def insert(self):
        db.session.add(self)
        db.session.commit()
    # update
    def update(self):
        db.session.commit()

    # delete
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_short(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def format_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
