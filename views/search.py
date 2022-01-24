from mymovielist import API_KEY, STATUSES, TYPES
from forms import EntryForm
from service import add_entry, delete_entry, edit_entry, get_entry, get_list
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user, login_required
from json import loads
from requests import get


bp = Blueprint('search', __name__)

@bp.route("/", methods=["GET"])
def index():
    """Render a landing page if user is not logged in."""
    if current_user.is_authenticated:
        return redirect(url_for('search.search'))
    else:    
        return render_template("landing.html")


@bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Render search page and handle search queries."""
    if request.method == "GET":
        return render_template("search.html")
    else:    
        # Send request to OMDB
        query = request.form.get("query")
        response = loads(get(f'http://www.omdbapi.com/?apikey={API_KEY}&s={query}').text)
        if response['Response'] == 'False':
            return render_template('searchres.html', apology=response['Error'])

        # Select only movies/series and remove duplicates
        rawresults = response['Search']
        results = []
        for result in rawresults:
            if result['Type'] in TYPES and result not in results:
                results.append(result)
        if len(results) == 0:
            return render_template('searchres.html', apology='Sorry, nothing found.')
        return render_template("searchres.html", results=results)          


@bp.route("/title/<imdb>", methods=["GET", "POST"])
@login_required
def title(imdb):
    """Render title page and handle add/edit/delete entry requests."""
    # Send request to OMDB
    titledata = loads(get(f'http://www.omdbapi.com/?apikey={API_KEY}&plot=full&i={imdb}').text)

    # Handle incorrect requests
    if titledata['Response'] == 'False':
        flash(titledata['Error'], 'danger')
        return redirect(url_for('search.search'))
    else:
        if current_user.is_authenticated:
            form = EntryForm()
            if form.validate_on_submit():
                # Add new entry to the db
                if request.form['submit'] == 'Add':
                    if form.status.data:
                        data = {'username': current_user.username,
                                'imdb': imdb,
                                'status': form.status.data,
                                'score': None if not form.score.data else int(form.score.data),
                                'type': titledata['Type'],
                                'title': titledata['Title'],
                                'year': titledata['Year']
                                }    
                        if not add_entry(data):
                            flash('Sorry, something went wrong.', 'danger')
                        return redirect(url_for('search.title', imdb=imdb))
                    else:
                        flash('Status is required', 'danger')     

                # Edit existing entry 
                elif request.form['submit'] == 'Edit':
                    if form.status.data or form.score.data:
                        data = {'username': current_user.username,
                                'imdb': imdb,
                                'status': form.status.data,
                                'score': None if not form.score.data else int(form.score.data),
                                }      
                        if not edit_entry(data):
                            flash('Sorry, something went wrong.', 'danger')
                        return redirect(url_for('search.title', imdb=imdb))
                    else:
                        flash('Provide status and/or score to update', 'danger') 

                # Delete existing entry
                elif request.form['submit'] == 'Delete':
                    if delete_entry(current_user.username, imdb):
                        return redirect(url_for('search.title', imdb=imdb))
                    else:
                        flash('Sorry, something went wrong.', 'danger')        

            # Display title page
            entry = get_entry(current_user.username, imdb)        
            if entry:
                return render_template("title.html", titledata=titledata, entry=entry, form=form)   
            else:
                return render_template("title.html", titledata=titledata, form=form)    


@bp.route("/mylist", methods=["GET", "POST"])
@login_required
def mylist():
    """Render user's lists and handle edit/delete entry requests."""
    form = EntryForm()
    if form.validate_on_submit():
        # Edit existing entry 
        if request.form['submit'] == 'Edit':
            # Ensure user provided status and/or score
            if form.status.data or form.score.data:
                data = {'username': current_user.username,
                        'imdb': request.form['imdb'],
                        'status': form.status.data,
                        'score': None if not form.score.data else int(form.score.data),
                        }      
                if not edit_entry(data):
                    flash('Sorry, something went wrong.', 'danger')
                return redirect(url_for('search.mylist'))
            else:
                flash('Provide status and/or score to update', 'danger')     

        # Delete existing entry
        elif request.form['submit'] == 'Delete':
            if delete_entry(current_user.username, request.form['imdb']):
                return redirect(url_for('search.mylist'))
            else:
                flash('Sorry, something went wrong.', 'danger')

    # Display user's lists
    lists = [get_list(current_user.username, status) for status in STATUSES]
    if (lists[0] or lists[1] or lists[2] or lists[3]):
        return render_template('mylist.html', lists=lists, form=form)
    return render_template('mylist.html')