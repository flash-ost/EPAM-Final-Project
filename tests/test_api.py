"""
Defines classes for testing API routes.
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import unittest
from mymovielist import db
from models import Entry, User, Movie
from tests import BaseTestCase


class UserApiCase(BaseTestCase):
    """
    Class for testing API User route.
    """
    def test_user_get(self):
        # Prepopulate db
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()

        # Test request with invalid credentials
        data = {'username': 'nonexist', 'password': 'nonexist'}
        response = self.client.get('/api/user', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test valid request
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.get('/api/user', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_user_post(self):
        # Test user registration
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post('/api/user', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test registering with the same username
        response = self.client.post('/api/user', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test registering with required data missing
        data = [{'password': 'testpass'},
                {'username': 'tst'},
                {'username': '', 'password': 'testpass'},
                {'username': 'tst', 'password': ''}
               ]
        for el in data:
            response = self.client.post('/api/user', data=json.dumps(el), content_type='application/json')
            self.assertEqual(response.status_code, 400)

   
class EntryApiCase(BaseTestCase):
    """
    Class for testing API Entry route.
    """
    def prepopulate(func):
        """Prepopulate db for testing."""
        def wrapper(self):
            user = User(username='testuser')
            user.set_password('testpass')
            db.session.add(user)
            movie = Movie(imdb='tt10872600', title='Spider-Man: No Way Home', type_id=1, year=2021)
            db.session.add(movie)
            entry = Entry(user_id=1, movie_id=1, status_id=1)
            db.session.add(entry)
            db.session.commit()
            return func(self)
        return wrapper

    @prepopulate
    def test_entry_get(self):
        # Test valid request
        data = {'username': 'testuser', 'password': 'testpass', 'imdb': 'tt10872600'}
        response = self.client.get('/api/entry', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test invalid requests
        data = [{'username': 'testuser', 'password': 'nonexist', 'imdb': 'tt10872600'},
                {'username': 'testuser', 'password': 'testpass', 'imdb': 'tt10872325'},
                {'username': 'testuser', 'password': 'nonexist', 'imdb': ''},
               ]
        for el in data:
            response = self.client.get('/api/entry', data=json.dumps(el), content_type='application/json')
            self.assertEqual(response.status_code, 400)


    @prepopulate
    def test_entry_put(self):
        # Test valid request
        data = {'username': 'testuser', 'password': 'testpass', 'imdb': 'tt10872600', 'status': 'Watching'}
        response = self.client.put('/api/entry', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test invalid requests
        data = [{'username': 'testuser', 'password': 'nonexist', 'imdb': 'tt10872600', 'status': 'Watching'},
                {'username': 'testuser', 'password': 'testpass', 'imdb': 'tt10872325', 'status': 'Watching'},
                {'username': 'testuser', 'password': 'nonexist', 'imdb': '', 'status': 'Watching'},
                {'username': 'testuser', 'password': 'nonexist', 'imdb': 'tt10872600'}
               ]
        for el in data:
            response = self.client.put('/api/entry', data=json.dumps(el), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    
    @prepopulate
    def test_entry_delete(self):
        # Test valid request
        data = {'username': 'testuser', 'password': 'testpass', 'imdb': 'tt10872600'}
        response = self.client.delete('/api/entry', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test invalid requests
        data = [{'username': 'testuser', 'password': 'nonexist', 'imdb': 'tt10872600'},
                {'username': 'testuser', 'password': 'testpass', 'imdb': 'tt10872325'},
                {'username': 'testuser', 'password': 'nonexist', 'imdb': ''},
               ]
        for el in data:
            response = self.client.delete('/api/entry', data=json.dumps(el), content_type='application/json')
            self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(verbosity=2)