"""
Defines class for testing CRUD operations with User model.
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from mymovielist import db
from models import User
import service as crud

from tests import BaseTestCase

class UserCase(BaseTestCase):
    def test_password_hashing(self):
        user = User(username='test')
        user.set_password('testpass')
        self.assertFalse(user.check_password('chestpass'))
        self.assertTrue(user.check_password('testpass'))


    def test_check_credentials(self):
        user = User(username='test')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        self.assertFalse(crud.check_credentials('chest', 'testpass'))
        self.assertFalse(crud.check_credentials('test', 'chestpass'))
        self.assertEqual(crud.check_credentials('test', 'testpass'), user)


    def test_check_username(self):   
        user = User(username='test')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        self.assertFalse(crud.check_username('nonexist'))
        self.assertEqual(crud.check_username('test'), user)


    def test_register_user(self):
        user = User(username='test')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        self.assertFalse(crud.register_user('test', 'testpass'))
        db.session.rollback()
        self.assertTrue(crud.register_user('test1', 'testpass'))    


if __name__ == '__main__':
    unittest.main(verbosity=2)        