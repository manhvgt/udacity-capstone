## Imports
import os
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
import json


## Loading environement variable
ENV_FILE = find_dotenv(raise_error_if_not_found = True)
if ENV_FILE:
    load_dotenv()

db_dns = os.getenv('DB_DNS')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_name_test = os.getenv('DB_NAME_TEST')
db_url = os.getenv('DB_URL')

## Setup DB
db = SQLAlchemy()


## DB Function
# Check if the environment variables are set
def validate_db():
    if db_dns is None:
        print("DB IP address and port are not set.")
        return False
    if db_user is None:
        print("DB user name is not set.")
        return False
    if db_password is None:
        print("DB user password is not set.")
        return False
    if db_name_test is None:
        print("Database name for testing is not set.")
        return False
    return True

# Setup DB
def setup_db(app, debug_mode):
    # update DB name base on test mode
    database_path = os.getenv('DB_URL')
    if debug_mode:
        if not validate_db():
            raise Exception("DB variable is not set!")
        database_name=db_name_test
        database_path ="postgresql://{}:{}@{}/{}".format(db_user, db_password, db_dns, database_name)

    # Config DB
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
    actor_ids = db.Column(ARRAY(db.Integer), nullable=True)


    def __init__(self, title, release_date, actor_ids=[], casting_site=None, revenue=0):
        self.title = title
        self.release_date = release_date
        self.actor_ids = actor_ids
        self.casting_site = casting_site
        self.revenue = revenue

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
    age = db.Column(db.Integer, nullable=True)
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
