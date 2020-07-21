import unittest

from app import app, db
from app.models import Actor, Movie, MovieCast

class CastingAgnecyTestCase(unittest.TestCase):
    def setup(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
        self.client = self.app.test_client


    def test_add_actor(self):
        # send request: add new actor to database
        new_actor = {
            'name': 'Sarah',
            'age': 25,
            'gender': 'female'
        }
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("success"), True)
        self.assertTrue(data.get('added_question'))

        # check that question persists in database
        question = Question.query.filter_by(question=self.new_question.get('question')).first()
        self.assertEqual(question.question, self.new_question.get('question'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()