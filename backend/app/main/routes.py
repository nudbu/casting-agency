from flask import jsonify, abort, request
import datetime

from app.main import bp
from app.models import db, Actor, Movie, MovieCast
from app.helpers import string_from_date, date_from_string
# from app.auth.auth import requires_auth, AuthError
PAGINATE_LIMIT_DEFAULT = 7

def paginate(request, selection):
  offset = request.args.get('page', 1, type=int)
  limit = request.args.get('limit', PAGINATE_LIMIT_DEFAULT, type=int)
  start_index = (offset - 1) * limit
  end_index = start_index + limit

  formatted_elements = [element.format() for element in selection[start_index:end_index]]
  return formatted_elements


@bp.route('/')
def welcome():
    return jsonify({
        'success': True,
        'message': 'Welcome to the Casting Agency API'
    })

@bp.route('/callback')
def welcome():
    return jsonify({
        'success': True,
        'message': 'Login successful'
    })


########## Actor Endpoints

## Add actor to db
@bp.route('/actors', methods=['POST'])
# @requires_auth('add:actors')
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
    try:
        db.session.add(actor)
        db.session.commit()
        formatted_actor = actor.format()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'added_actor': formatted_actor,
    })

## Get Actors paginated
@bp.route('/actors')
# @requires_auth('get:actors')
def get_all_actors():
    actors = Actor.query.order_by(Actor.name).all()
    formatted_actors_page = paginate(request, actors)

    # handle page number out of range
    if not formatted_actors_page:
        abort(404)

    return jsonify({
        'success': True,
        'actors': formatted_actors_page,
        'total_actors': len(actors)
    })


## Delete Actor
@bp.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    formatted_actor = actor.format()

    # delete from db
    try:
        db.session.delete(actor)
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'deleted_actor': formatted_actor,
        'total_actors': Actor.query.count()
    })


## Update Actor Info
@bp.route('/actors/<int:actor_id>', methods=['PATCH'])
def update_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)

    # access request data
    try:
        body = request.get_json()
        name = body.get('name', None)
        birthdate_string = body.get('birthdate', None)
        gender = body.get('gender', None)
    except:
        abort(422)

    # update values; if none is given abort 422
    if any([name, birthdate_string, gender]):
        if name:
            actor.name = name
        if gender:
            actor.gender = gender
        if birthdate_string:
            actor.birthdate = date_from_string(birthdate_string)  
    else:
        abort(422)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    actor = Actor.query.get(actor_id)
    formatted_actor = actor.format()

    return jsonify({
        'success': True,
        'updated_actor': formatted_actor
    })

########## Movie Endpoints

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
    try:
        db.session.add(movie)
        db.session.commit()
        formatted_movie = movie.format()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'added_movie': formatted_movie,
    })

## Get Movies paginated
@bp.route('/movies')
def get_all_movies():
    movies = Movie.query.order_by(Movie.title).all()
    formatted_movies_page = paginate(request, movies)

    # handle page number out of range
    if not formatted_movies_page:
      abort(404)

    return jsonify({
        'success': True,
        'movies': formatted_movies_page,
        'total_movies': len(movies)
    })

## Delete Movie
@bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    formatted_movie = movie.format()

    try:
        db.session.delete(movie)
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'deleted_movie': formatted_movie,
        'total_movies': Movie.query.count()
    })

## Update Movie Info
@bp.route('/movies/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    # access request data
    try:
        body = request.get_json()
        title = body.get('title', None)
        release_date_string = body.get('release_date', None)
    except:
        abort(422)

    # update values; if none is specified abort 422
    if any([title, release_date_string]):
        if title:
            movie.title = title
        if release_date_string:
            movie.release_date = date_from_string(release_date_string)
    else:
        abort(422)

    formatted_movie = movie.format()

    try:
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'updated_movie': formatted_movie
    })

########## Booking Endpoints

## book Actor for Movie

@bp.route('/contracts', methods=['POST'])
def add_contract():
    #access request data
    try:
        body = request.get_json()
        movie_id = body['movie_id']
        actor_id = body['actor_id']
    except:
        abort(422)

    # 404, if movie or actor doesn't exist
    movie = Movie.query.get_or_404(movie_id)
    actor = Actor.query.get_or_404(actor_id)

    # add contract
    contract = MovieCast(actor_id=actor_id, movie_id=movie_id)
    try:
        db.session.add(contract)
        db.session.commit()
        formatted_contract = contract.format()
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'added_contract': formatted_contract,
    })