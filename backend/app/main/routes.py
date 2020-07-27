from flask import jsonify, abort, request
import datetime

from app.main import bp
from app.models import db, Actor, Movie, MovieCast



PAGINATE_LIMIT_DEFAULT = 7

def paginate(request, selection):
  offset = request.args.get('offset', 1, type=int)
  limit = request.args.get('limit', PAGINATE_LIMIT_DEFAULT, type=int)
  start_index = (offset - 1) * limit
  end_index = start_index + limit

  formatted_elements = [element.format() for element in selection[start_index:end_index]]
  return formatted_elements

def date_from_string(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d')

#### Actor Endpoints

## Add actor to db
@bp.route('/actors', methods=['POST'])
def add_actor():

    # access request data
    try:
        body = request.get_json()
        name = body.get('name', None)
        birthdate_string = body.get('birthdate')
        birthdate = date_from_string(birthdate_string)
        gender = body.get('gender', None)
    except:
        abort(422)

    actor = Actor(name=name, birthdate=birthdate, gender=gender)
    db.session.add(actor)
    db.session.commit()
    actor_id = actor.id

    return jsonify({
        'success': True,
        'added actor': name,
        'actor_id': actor_id
    })

## Get Actors paginated
@bp.route('/actors')
def get_all_actors():
    actors = Actor.query.order_by(Actor.name).all()
    formatted_actors_page = paginate(request, actors)

    return jsonify({
        'success': True,
        'actors': formatted_actors_page,
        'total_actors': len(actors)
    })


## Delete Actor
@bp.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    return jsonify({
        'success': True,
        'deleted_actor': actor_id,
        'total_actors': Actor.query.count()
    })


## Update Actor Info


#### Movie Endpoints

## Add movie to db
@bp.route('/movies', methods=['POST'])
def add_movie():

    #access request data
    try:
        body = request.get_json()
        title = body.get('title', None)
        release_date_string = body.get('release_date')
        release_date = date_from_string(release_date_string)
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

## Get Movies paginated
@bp.route('/movies')
def get_all_movies():
    movies = Movie.query.order_by(Movie.title).all()
    formatted_movies_page = paginate(request, movies)

    return jsonify({
        'success': True,
        'movies': formatted_movies_page,
        'total_movies': len(movies)
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