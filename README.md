# EPAM Final Project: MyMovieList
---
## Tabe of Contents
- [Overview](#overview)
- [How to Use](#how-to-use)
- [License](#license)
---
# Description
MyMovielist is a web app that allows users to keep track of their movies and TV shows.
### Structure
1) migrations — migration files to manage database schema changes
2) models — modules with Python classes describing DB models
3) service — modules with functions / classes to work with DB (CRUD operations)
5) rest — modules with RESTful service implementation
6) templates — web app html templates
7) static — static files (css)
8) tests — modules with unit tests
9) views — modules with Web controllers / views
---
### Authentication
Upon arriving on the landing page user is asked to log in. If user doesn't have an account yet, there is also a link to the registration page.
![auth](https://user-images.githubusercontent.com/41839630/149951681-8776705e-2a46-46b1-bc9b-b15b0c680ac0.png)

### Web app tabs
#### Search tab
After successful authentication user is redirected to the search page. Search results are clickable and have popover posters.
![search](https://user-images.githubusercontent.com/41839630/149953587-c5162875-24ce-477a-a65d-8caece2daf61.jpg)

If the user clicks on one of the search results, app redirects to that title's page. There user can check the title's info and add it to his/her list, specifying watching status and optionally a score.
![titleadd](https://user-images.githubusercontent.com/41839630/149957386-79ed3d54-abba-41a0-8109-a99be0dac37f.jpg)

If the title is already in user's list, there is an info box, indicating user's watching status and score. User can edit them or delete entry.
![titleedit](https://user-images.githubusercontent.com/41839630/149957887-e42dbd3a-4efe-426d-96e5-f475a28952e4.jpg)

