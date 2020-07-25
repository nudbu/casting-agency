import unittest
import json

from app import create_app, db
from app.models import Actor, Movie, MovieCast
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


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_add_actor(self):
        # send request: add new actor to database
        new_actor = {
            'name': 'Sarah',
            'age': 25,
            'gender': 'female'
        }
        res = self.client().post('/actors', json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get('added actor'))

        # check that actor persists in database
        actor = Actor.query.filter_by(name=new_actor.get('name')).first()
        self.assertEqual(actor.name, new_actor.get('name'))



    def test_add_movie(self):
        # send request: add new movie to database
        new_movie = {
            'title': 'Harry Potter and the Philosophers Stone',
            'release_date': '2001-11-04',
        }
        res = self.client().post('/movies', json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get('added movie'))

        # check that actor persists in database
        movie = Movie.query.filter_by(title=new_movie.get('title')).first()
        self.assertEqual(movie.title, new_movie.get('title'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()