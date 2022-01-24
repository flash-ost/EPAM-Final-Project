import service as crud

from mymovielist import API_KEY, STATUSES
from flask import request
from flask_restful import reqparse, Resource
from json import loads
from os import environ
from requests import get


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='Your username (required)', required=True)
parser.add_argument('password', type=str, help='Your password (required)', required=True)
parser.add_argument('imdb', type=str, help='IMDB ID of title')
parser.add_argument('status', type=str, help=f'Your watching status: {STATUSES}', choices=STATUSES)
parser.add_argument('score', type=int, default=None, help='Your score from 1 to 10 (optional)', choices=[i for i in range(1, 11)])


def authorize(func):
    """Ensure user provided IMDB ID and valid credentials."""
    def wrapper(self):
        global args 
        args = parser.parse_args()

        # Handle invalid credentials
        if not crud.check_credentials(args['username'], args['password']):
            return {'message': 'Invalid username or password'}, 400

        # Handle absent IMDB ID
        if 'entry' in request.base_url and not args['imdb']:
            return {'message': 'IMDB ID is required'}, 400
        return func(self)
    return wrapper


class User(Resource):
    """Functions to get user's lists (get) and register a user (post)."""
    @authorize
    def get(self):
        """Return user's lists."""
        lists = [crud.get_list(args['username'], status) for status in STATUSES]
        final = [[{'IMDB': entry.movie.imdb, 
                   'Title': entry.movie.title, 
                   'Type': entry.movie.type.type_name,
                   'Year': entry.movie.year,
                   'Score': entry.score} for entry in list] for list in lists]
        response = dict(zip(STATUSES, final))
        return response


    def post(self):
        """Register a user."""
        args = parser.parse_args()
        # Handle missing credentials
        if not args['username'] or not args['password']:
            return {'message': "Credentials can't be empty"}, 400

        # Handle duplicate username
        if crud.check_username(args['username']):
            return {'message': 'This username is already taken'}, 400

        # Register
        if crud.register_user(args['username'], args['password']):
            return {'message': 'User successfully registered'}
        else:
            return {'message': 'Sorry, something went wrong'}, 500

    
class Entry(Resource):
    """Functions to create (post), update (put), and delete entries."""
    @authorize
    def get(self):
        """Get a single entry."""
        entry = crud.get_entry(args['username'], args['imdb'])
        if not entry:
            return {'message': "Entry doesn't exist"}, 400
        else:
            response = {'IMDB': entry.movie.imdb, 
                        'Title': entry.movie.title, 
                        'Type': entry.movie.type.type_name,
                        'Year': entry.movie.year,
                        'Status': entry.status.status_name,
                        'Score': entry.score
                       }
            return response           


    @authorize
    def post(self):
        """Create a new entry."""
        # Ensure user provided a status
        if not args['status']:
            return {'message': 'Status is required'}, 400

        # Ensure user provided a valid IMDB ID
        titledata = loads(get(f'http://www.omdbapi.com/?apikey={API_KEY}&plot=short&i={args["imdb"]}').text)
        if titledata['Response'] == 'False':
            return {'message': titledata['Error']}, 400

        # Check if such entry already exists
        if crud.get_entry(args['username'], args['imdb']):
            return {'message': 'Entry already exists. Use [put] request if you want to update.'}, 418

        # Add entry to the database
        data = {'username': args['username'],
                'imdb': args['imdb'],
                'status': args['status'],
                'score': args['score'],
                'type': titledata['Type'],
                'title': titledata['Title'],
                'year': titledata['Year']
                }    
        if (crud.add_entry(data)):
            return {'message': 'Entry successfully added'}
        else:
            return {'message': 'Sorry, something went wrong'}, 500


    @authorize
    def put(self):
        """Update existing entry."""
        # Ensure user provided status or score
        if not args['status'] and not args['score']:
            return {'message': 'Provide status and/or score to update'}, 400
        
        # Ensure entry exists
        if not crud.get_entry(args['username'], args['imdb']):
            return {'message': "Entry doesn't exist"}, 400
        
        # Update entry
        data = {'username': args['username'],
                'imdb': args['imdb'],
                'status': args['status'],
                'score': args['score']
                }
        if crud.edit_entry(data):
            return {'message': 'Entry successfully updated'}
        else:
            return {'message': 'Sorry, something went wrong'}, 500

    @authorize
    def delete(self):
        """Delete entry."""
        # Ensure entry exists
        if not crud.get_entry(args['username'], args['imdb']):
            return {'message': "Entry doesn't exist"}, 400
        
        # Delete entry
        if crud.delete_entry(args['username'], args['imdb']):
            return {'message': 'Entry successfully deleted'}
        else:
            return {'message': 'Sorry, something went wrong'}, 500        