from flask import jsonify
import datetime

from app import app
from app.models import db, Actor, Movie

### Actor Endpoints


## Add actor to db
@app.route('/actors', methods=['POST'])
def add_actor():
    actor = Actor(name='sandra', age=25, gender='other')
    db.session.add(actor)
    db.session.commit()
    return jsonify({
        'test': 'this is a test'
    })


## Get all actors
@app.route('/actors')
def get_actors():
    actors = Actor.query.all()
    return jsonify({
        'test': 'test'
    })

### Movie Endpoints

## Add movie to db
@app.route('/movies', methods=['POST'])
def add_movie():
    release_date = datetime.datetime(2001, 11, 4)
    movie = Movie(title='harry potter', release_date=release_date)
    db.session.add(movie)
    db.session.commit()
    return jsonify({
        'added movie': 'harry potter'
    })

