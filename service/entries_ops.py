"""
Contains functions for CRUD operations with Entry model.
"""

from mymovielist import db, STATUSES, TYPES
from models import Entry, Movie, Status, Type, User


def add_entry(data):
    """Add new entry to the db."""
    # Ensure movie is in the db."""
    movie = check_movie(data['imdb'])
    if not movie:
        movie = add_movie(data)

    # Add new antry
    try:
        status = Status.query.filter_by(status_name=data['status']).first()
        user = User.query.filter_by(username=data['username']).first()
        newentry = Entry(owner=user, movie=movie, status=status, score=data['score'])
        db.session.add(newentry)
        db.session.commit()
        return newentry
    except:
        return False


def get_entry(username, imdb):
    """Return entry from the db."""
    entry = Entry.query.filter(Entry.owner.has(username=username), Entry.movie.has(imdb=imdb)).first()
    return entry if entry else False


def edit_entry(data):
    """Change entry's status and/or score."""
    try:
        entry = get_entry(data['username'], data['imdb'])
        if data['status']:
            entry.status = Status.query.filter_by(status_name=data['status']).first()
        if data['score']:
            entry.score = data['score']
        db.session.add(entry)    
        db.session.commit() 
        return entry
    except:
        return False


def delete_entry(username, imdb):
    """Delete entry from the db."""
    try:
        entry = get_entry(username, imdb)
        db.session.delete(entry)  
        db.session.commit()
        return entry
    except:
        return False         


def get_list(username, status):
    """Return user's list of entries with given status."""
    list = Entry.query.filter(Entry.owner.has(username=username), Entry.status.has(status_name=status)).all()
    return list


def add_movie(data):
    """Add new movie to the db."""
    try:
        type = Type.query.filter_by(type_name=data['type']).first()
        newmovie = Movie(imdb=data['imdb'], title=data['title'], type=type, year=data['year'])
        db.session.add(newmovie)
        db.session.commit()
        return newmovie
    except:
        return False 


def check_movie(imdb):
    """Check whether given movie exists in the db."""
    movie = Movie.query.filter_by(imdb=imdb).first()
    return movie             


def populate_db():
    """Populate db with statuses and types."""
    for status in STATUSES:
        s = Status(status_name=status)
        db.session.add(s) 
    for type in TYPES:
        t = Type(type_name=type)
        db.session.add(t)
    db.session.commit()