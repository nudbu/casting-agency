from enum import Enum
from datetime import date
from app import db
from app.helpers import string_from_date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class Gender(Enum):
    female = 1
    male = 2
    other = 3

class Actor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  birthdate = db.Column(db.Date, nullable=False)
  gender = db.Column(db.Enum(Gender), nullable=False)
  movies = db.relationship('MovieCast', backref='ac')

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': calculate_age(self.birthdate),
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
