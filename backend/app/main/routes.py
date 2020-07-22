from flask import jsonify, abort, request
import datetime

from app.main import bp
from app.models import db, Actor, Movie

#### Actor Endpoints


## Add actor to db
@bp.route('/actors', methods=['POST'])
def add_actor():

    # access request data
    try:
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
    except:
        abort(422)

    actor = Actor(name=name, age=age, gender=gender)
    db.session.add(actor)
    db.session.commit()
    return jsonify({
        'success': True,
        'added actor': name
    })


## Get all actors
@bp.route('/actors')
def get_actors():
    actors = Actor.query.all()
    return jsonify({
        'test': 'test'
    })


#### Movie Endpoints

## Add movie to db
@bp.route('/movies', methods=['POST'])
def add_movie():

    #access request data
    body = request.get_json()
    title = body.get('title', None)
    release_date_string = body.get('release_date')
    release_date = datetime.datetime.strptime(release_date_string, '%Y-%m-%d')

    movie = Movie(title=title, release_date=release_date)
    db.session.add(movie)
    db.session.commit()
    return jsonify({
        'success': True,
        'added movie': title
    })
