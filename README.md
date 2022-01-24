# EPAM Final Project: MyMovieList
---
## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [API Routes](#api-routes)
- [Author Info](#author-info)
---
## Overview
MyMovieList is a web app that allows users to keep track of their movies and TV shows.
### Structure
- migrations — migration files to manage database schema changes
- models — modules with Python classes describing DB models
- service — modules with functions / classes to work with DB (CRUD operations)
- rest — modules with RESTful service implementation
- templates — web app html templates
- static — static files (css)
- tests — modules with unit tests
- views — modules with Web controllers / views
---
### Authentication
Upon arriving on the landing page user is asked to log in. There is a link to the registration page for those who don't have an account yet.
![auth](https://user-images.githubusercontent.com/41839630/150019698-a2bcdbd4-ef56-4203-b009-ec9abe8a38c6.jpg)

### Web app tabs
#### Search tab
After successful authentication user is redirected to the search tab. Search results are clickable and have popover posters.
![search](https://user-images.githubusercontent.com/41839630/149953587-c5162875-24ce-477a-a65d-8caece2daf61.jpg)

If the user clicks on one of the search results, app redirects to that title's page. There user can check the title's info and add it to his/her list, specifying watching status and optionally a score.
![titleadd](https://user-images.githubusercontent.com/41839630/150017115-d7748c0e-1f25-4c36-8f8c-8e6dd35ae391.jpg)

If the title is already in user's list, there is an info box indicating user's watching status and score. User can edit them or delete entry.
![titleedit](https://user-images.githubusercontent.com/41839630/150028944-7d677e95-5aa5-4604-bf55-005161ad3269.jpg)

#### My Lists tab
The second tab is where all of user's lists are displayed. Every entry also has edit and delete button.
![list](https://user-images.githubusercontent.com/41839630/150019408-bdfa28ad-efc2-43b0-8326-68cc8aa2892f.jpg)

## Setup
1) Install Python.
```
    https://www.youtube.com/watch?v=bXWlyOMYpRE
```
2) Install necessary packages with command:
```
    pip install -r requirements.txt
```
3) App uses a third-party OMDb API to get information about titles, so you need to request an API key via this form:
```
    http://www.omdbapi.com/apikey.aspx
```
  After you receive the key export it to app's environment with this command:
```
    export API_KEY=value
```
4) Create a db with the following command:
```
    flask db upgrade
```
5) Call Flask shell
```
    flask shell
```
and pre-populate two columns of the db by running:
```
    from service import populate_db
    populate_db()
```
6) Set the app name in the environment
```
    export FLASK_APP=mymovielist.py
```
and run the app with
```
    flask run
```

## Api Routes
/api/user  
- GET — get a list of user's entries sorted by watching status  
- POST — register a new user
```
    {"username": "", "password": ""}
```
/api/entry  
- GET — get entry's info by IMDB ID in json format  
- DELETE — delete entry
```
    {"username": "", "password": "", "imdb": ""}
```
- POST — create new entry  
- PUT — update entry's status and/or score
```
    {"username": "", "password": "", "imdb": "", "status": "", "score": ""}
```

## Author Info
- Name: Ostap Marushchak
- Email: ost.marushchak@gmail.com
- License: MIT
