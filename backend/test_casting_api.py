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


    def test_add_actor(self):
        # send request: add new actor to database
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get('added actor'))

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

############# Movies

    def test_add_movie(self):
        # send request: add new movie to database
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get('added movie'))

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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()