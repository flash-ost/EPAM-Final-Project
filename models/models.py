from mymovielist import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    hash = db.Column(db.String(128), nullable=False)
    entries = db.relationship('Entry', backref='owner', cascade="all,delete")

    def set_password(self, password):
        self.hash = generate_password_hash(password)    

    def check_password(self, password):
        return check_password_hash(self.hash, password)    


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    score = db.Column(db.Integer, nullable=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb = db.Column(db.String(15), index=True, nullable=False, unique=True)
    title = db.Column(db.String(250), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    entries = db.relationship('Entry', backref='movie')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(20), index=True, nullable=False, unique=True)
    entries = db.relationship('Entry', backref='status')


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(6), index=True, nullable=False, unique=True)
    movies = db.relationship('Movie', backref='type')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
