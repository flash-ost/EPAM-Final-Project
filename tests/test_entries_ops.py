"""
Defines class for testing CRUD operations with Entry model.
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from mymovielist import db
from models import Entry, Movie, User
import service as crud

from tests import BaseTestCase


class EntryCase(BaseTestCase):
    def test_get_entry(self):
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        movie = Movie(imdb='testmovie', title='testmovie', type_id=1, year=2000)
        db.session.add(movie)
        entry = Entry(user_id=1, movie_id=1, status_id=1)
        db.session.add(entry)
        db.session.commit()
        self.assertFalse(crud.get_entry('testuser', 'nonexist'))
        self.assertFalse(crud.get_entry('nonexist', 'testmovie'))
        self.assertTrue(crud.get_entry('testuser', 'testmovie'))


    def test_add_entry(self):
        # Prepopulate db
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        movie = Movie(imdb='testmovie', title='testmovie', type_id=1, year=2000)
        db.session.add(movie)
        db.session.commit()

        # Test adding entry without required data
        data = {'imdb': 'testmovie', 'status': 'Completed', 'username': 'testuser', 'score': 10}
        for el in data:
            tmp = data[el]
            data[el] = None
            self.assertTrue(crud.add_entry(data)) if el == 'score' else self.assertFalse(crud.add_entry(data))
            db.session.rollback()
            data[el] = tmp

        # Test adding entry with score
        data['score'] = 10 
        self.assertTrue(crud.add_entry(data))


    def test_edit_entry(self):
        # Prepopulate db
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        movie = Movie(imdb='testmovie', title='testmovie', type_id=1, year=2000)
        db.session.add(movie)
        entry = Entry(user_id=1, movie_id=1, status_id=1)
        db.session.add(entry)
        db.session.commit()

        # Test editing non-existing entry
        data = {'username': 'nonexist', 'imdb': 'testmovie', 'status': 'Completed', 'score': 10}
        self.assertFalse(crud.edit_entry(data))
        db.session.rollback()

        # Test editing exisitng entry
        data['username'] = 'testuser'
        self.assertTrue(crud.edit_entry(data))


    def test_delete_entry(self):
        # Prepopulate db
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        movie = Movie(imdb='testmovie', title='testmovie', type_id=1, year=2000)
        db.session.add(movie)
        entry = Entry(user_id=1, movie_id=1, status_id=1)
        db.session.add(entry)
        db.session.commit()

        # Test deleting non-existing entry
        self.assertFalse(crud.delete_entry('nonexist', 'nonexist'))
        db.session.rollback()

        # Test deleting exisitng entry
        self.assertTrue(crud.delete_entry('testuser', 'testmovie'))


    def test_get_list(self):
        # Prepopulate db
        user = User(username='testuser')
        user.set_password('testpass')
        db.session.add(user)
        movie1 = Movie(imdb='testmovie', title='testmovie', type_id=1, year=2000)
        movie2 = Movie(imdb='testmovie2', title='testmovie2', type_id=1, year=2000)
        db.session.add(movie1)
        db.session.add(movie2)
        entry1 = Entry(user_id=1, movie_id=1, status_id=1)
        entry2 = Entry(user_id=1, movie_id=2, status_id=1)
        db.session.add(entry1)
        db.session.add(entry2)
        db.session.commit()

        # Test getting a list
        self.assertEqual(crud.get_list('testuser', 'Plan To Watch'), [entry1, entry2])


    def test_check_movie(self):   
        movie = Movie(imdb='testmovie', title='testmovie', type_id=1, year=2000)
        db.session.add(movie)
        db.session.commit()
        self.assertFalse(crud.check_movie('nonexist'))
        self.assertTrue(crud.check_movie('testmovie'))


    def test_add_movie(self):
        data = {'imdb': 'testmovie', 'title': 'testtitle', 'type': 'movie', 'year': 2000}
        for el in data:
            tmp = data[el]
            data[el] = None
            self.assertFalse(crud.add_movie(data))
            db.session.rollback()
            data[el] = tmp
        self.assertTrue(crud.add_movie(data))


if __name__ == '__main__':
    unittest.main(verbosity=2)