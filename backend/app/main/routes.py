from flask import jsonify, abort, request
import datetime

from app.main import bp
from app.models import db, Actor, Movie, MovieCast

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
    actor_id = actor.id

    return jsonify({
        'success': True,
        'added actor': name,
        'actor_id': actor_id
    })

#### Movie Endpoints

## Add movie to db
@bp.route('/movies', methods=['POST'])
def add_movie():

    #access request data
    try:
        body = request.get_json()
        title = body.get('title', None)
        release_date_string = body.get('release_date')
        release_date = datetime.datetime.strptime(release_date_string, '%Y-%m-%d')
    except:
        abort(422)

    movie = Movie(title=title, release_date=release_date)
    db.session.add(movie)
    db.session.commit()
    movie_id = movie.id

    return jsonify({
        'success': True,
        'added movie': title,
        'movie_id': movie_id
    })


#### Booking Endpoints

## book Actor for Movie

@bp.route('/contracts', methods=['POST'])
def add_contract():
    #access request data
    try:
        body = request.get_json()
        movie_id = body.get('movie_id', None)
        actor_id = body.get('actor_id', None)
    except:
        abort(422)

    contract = MovieCast(actor_id=actor_id, movie_id=movie_id)
    db.session.add(contract)
    db.session.commit()

    return jsonify({
        'success': True,
        'added contract': 'id',
        'movie_id': movie_id,
        'actor_id': actor_id 
    })