from enum import Enum
from app import db


class Gender(Enum):
    female = 1
    male = 2
    other = 3

class Actor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.Enum(Gender), nullable=False)
  movies = db.relationship('MovieCast', backref='ac')

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender.name
    }


class Movie(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(), nullable=False)
  release_date = db.Column(db.Date, nullable=False)
  cast = db.relationship('MovieCast', backref='mov')

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }


## Junction Table for many-to-many relationship between Actors and Movies
class MovieCast(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
  movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
