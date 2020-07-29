import unittest
import json

from app import create_app, db
from app.models import Actor, Movie, MovieCast
from app.helpers import string_from_date
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client

        # insert mock data to test on 

        self.new_actor = {
            "name": "Sandra",
            "birthdate": "1995-12-30",
            "gender": "female"
        }

        self.new_movie = {
            'title': 'Harry Potter and the Philosophers Stone',
            'release_date': '2001-11-04',
        }

        res = self.client().post('/actors', json=self.new_actor)
        res = self.client().post('/movies', json=self.new_movie)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


############# Actors

    def test_get_paginated_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('total_actors'))
        self.assertTrue(len(data['actors']))
    
    def test_404_beyond_valid_actor_page(self):
        res = self.client().get('/actors?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data.get('message'))

    def test_add_actor(self):
        # send request: add new actor to database
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get('added_actor'))

        # check that actor persists in database
        actor = Actor.query.filter_by(name=self.new_actor.get('name')).first()
        self.assertEqual(actor.name, self.new_actor.get('name'))


    def test_422_if_actor_creation_failed(self):
        res = self.client().post('/actors', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


    def test_patch_actor(self):
        updated_actor = {
            'name': 'Sue',
            'birthdate': '1994-11-04',
        }

        res = self.client().patch('/actors/1', json=updated_actor)
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get("updated_actor"))
        # check persistance in db
        actor = Actor.query.get(1)
        self.assertEqual(actor.name, updated_actor.get('name'))
        self.assertEqual(string_from_date(actor.birthdate), updated_actor.get('birthdate'))


    def test_422_if_actor_patch_failed(self):
        res = self.client().patch('/actors/1', json={})
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data.get("success"), False)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('deleted_actor'))
        self.assertTrue(type(data.get('total_actors')) is int)

    def test_404_delete_non_existing_actor(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)



############# Movies

    def test_get_paginated_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('total_movies'))
        self.assertTrue(len(data['movies']))
    
    def test_404_beyond_valid_movie_page(self):
        res = self.client().get('/movies?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data.get('message'))

    def test_add_movie(self):
        # send request: add new movie to database
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get('added_movie'))

        # check that movie persists in database
        movie = Movie.query.filter_by(title=self.new_movie.get('title')).first()
        self.assertEqual(movie.title, self.new_movie.get('title'))


    def test_422_if_movie_creation_failed(self):
        res = self.client().post('/movies', json={})
        self.assertEqual(res.status_code, 422)


    def test_patch_movie(self):
        updated_movie = {
            'title': 'Fight Club',
            'release_date': '2005-11-04',
        }

        res = self.client().patch('/movies/1', json=updated_movie)
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get("updated_movie"))
        # check persistance in db
        movie = Movie.query.get(1)
        self.assertEqual(movie.title, updated_movie.get('title'))
        self.assertEqual(string_from_date(movie.release_date), updated_movie.get('release_date'))


    def test_422_if_movie_patch_failed(self):
        res = self.client().patch('/movies/1', json={})
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data.get("success"), False)


    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('deleted_movie'))
        self.assertTrue(type(data.get('total_movies')) is int)

    def test_404_delete_non_existing_movie(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)


############# Contracts

    def test_add_contract(self):
        new_contract = {
            "actor_id": 1,
            "movie_id": 1
        }
        res = self.client().post('/contracts', json=new_contract)
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('added_contract'))


    def test_404_failed_to_add_contract(self):
        # 404 if movie or actor doesn't exist
        new_contract = {
            "actor_id": 1,
            "movie_id": 1000
        }
        res = self.client().post('/contracts', json=new_contract)
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)


    def test_422_failed_to_add_contract(self):
        # 422 if movie if or actor id not given
        new_contract = {
            "actor_id": 1,
        }
        res = self.client().post('/contracts', json=new_contract)
        data = json.loads(res.data)
        # check response
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data.get('success'), False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()