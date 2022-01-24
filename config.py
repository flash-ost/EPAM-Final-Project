"""
Module contains configuration variables.
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mml.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Make sure API key is set
    API_KEY = os.environ.get("API_KEY")
    if not API_KEY:
        raise RuntimeError("API_KEY not set")
