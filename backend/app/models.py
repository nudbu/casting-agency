from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from enum import Enum
from app import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Gender(Enum):
    female = 1
    male = 2
    other = 3

class Actor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.Enum(Gender), nullable=False)
  movies = db.relationship('Movie_Cast', backref='ac')

class Movie(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(), nullable=False)
  release_date = db.Column(db.Date, nullable=False)
  cast = db.relationship('Movie_Cast', backref='mov')


## Junction Table for many to many relationship between Actors and Movies
class MovieCast(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
  movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)