"""
Contains functions for CRUD operations with User model.
"""

from mymovielist import db
from models import User


def check_credentials(username: str, password: str):
    """Check whether user provided valid credentials."""
    user = check_username(username)
    if not user or not user.check_password(password):
        return False
    return user


def check_username(username: str):
    """Check whether given username exists in the db."""
    user = User.query.filter_by(username=username).first()
    return user if user else False


def register_user(username, password):
    """Register a user."""
    try:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return True
    except:
        return False 