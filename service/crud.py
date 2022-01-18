from mymovielist import db, STATUSES, TYPES
from models.models import Entry, Movie, Status, Type, User


def check_credentials(username: str, password: str):
    """Check whether user provided valid credentials."""
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return False
    return user


def check_username(username: str):
    """Check whether given username exists in the db."""
    user = User.query.filter_by(username=username).first()
    return True if user else False


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


def get_entry(username, imdb):
    """Return entry from the db."""
    entry = Entry.query.filter_by(owner=User.query.filter_by(username=username).first(), 
        movie = check_movie(imdb)).first()                            
    return entry


def check_movie(imdb):
    """Check whether given movie exists in the db."""
    movie = Movie.query.filter_by(imdb=imdb).first()
    return movie


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


def get_list(username, status):
    """Return user's list of entries with given status."""
    list = Entry.query.filter(Entry.owner.has(username=username), Entry.status.has(status_name=status)).all()
    return list


def delete_entry(username, imdb):
    """Delete entry from the db."""
    try:
        entry = get_entry(username, imdb)
        db.session.delete(entry)  
        db.session.commit()
        return entry
    except:
        return False       


def populate_db():
    """Populate db with statuses and types."""
    for status in STATUSES:
        s = Status(status_name=status)
        db.session.add(s) 
    for type in TYPES:
        t = Type(type_name=type)
        db.session.add(t)
    db.session.commit()