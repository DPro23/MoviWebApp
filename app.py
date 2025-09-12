from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, url_for
from data_manager import DataManager
from models import db, Movie
import requests
import os

# load secrets from .env
load_dotenv()

# Formatting the API url
API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
API_URL = f"{API_BASE_URL}?apikey={API_KEY}&"

# Database path
MOVIES_DB = 'data/movies.db'

# Flask object
app = Flask(__name__)

# ORM configuration (SQLAlchemy)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, MOVIES_DB)}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect db and flask
db.init_app(app)

# DataManager object
data_manager = DataManager()

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler"""
    return "<div><h1>404</h1><a href='/'>Back home</a></div>", 404


@app.route('/')
def index():
    """
    Home page. Show a list of
    all registered users and
    a form for adding new users
    """
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Adds new user to the database, then redirects back to home"""
    username = request.form['username'].strip()
    if username:
        data_manager.create_user(username)
        return redirect(url_for('index', success=f'{username} registered!'))
    # Invalid username, render with an error message
    return redirect(url_for('index', error='Invalid username!'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """Shows user's movies"""
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', user_id=user_id, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Adds a new movie to a user’s list of movies.
    It generates a Movie object filled with infos
    fetched by OMDb API
    """
    try:
        input_name = request.form['name'].strip()

        if input_name == '':
            error = 'Invalid title!'
            return redirect(url_for('list_movies', user_id=user_id, error=error))

        # fetch from API by input_name as param
        query_params = {
            "type": "movie",
            't': input_name,
            'plot': 'full'
        }

        # Fetch movies data from OMDbAPI
        api_result = requests.get(API_URL, params=query_params).json()

        # Movie not found
        if api_result['Response'] == 'False' or len(api_result) == 0:
            error = 'Movie not found!'
            return redirect(url_for('list_movies', user_id=user_id, error=error))

        # Define initial Movie object attributes
        new_movie = {
            "name": input_name,
            "director": '',
            "year": 0,  # int
            "poster_url": '',  # string
            "user_id": user_id  # int
        }

        if 'Title' in api_result:
            book_name = api_result['Title'].strip()
            if book_name == '':
                error = 'Invalid title!'
                return redirect(url_for('list_movies', user_id=user_id, error=error))

            new_movie['name'] = book_name

        # Stops if movie is already in the database
        if new_movie['name'] in data_manager.get_movies(user_id):
            error = f'Movie {new_movie["name"]} already exists!'
            return redirect(url_for('list_movies', user_id=user_id, error=error))

        if 'Year' in api_result:
            year = api_result['Year'].strip()
            if year.isdigit():
                new_movie['year'] = int(year)
            else:
                error = 'Sorry, invalid year format from API!'
                return redirect(url_for('list_movies', user_id=user_id, error=error))

        if 'Director' in api_result:
            director = api_result['Director'].strip()
            if director == '':
                error = "Can't find director for this movie!"
                return redirect(url_for('list_movies', user_id=user_id, error=error))

            new_movie['director'] = director

        if 'Poster' in api_result:
            poster_url = api_result['Poster'].strip()
            if poster_url == '':
                error = "Can't find poster for this movie!"
                return redirect(url_for('list_movies', user_id=user_id, error=error))

            new_movie['poster_url'] = poster_url

        success = f'Movie "{new_movie["name"]}" added!'

        # Create the Movie object
        new_movie = Movie(
            name=new_movie['name'],
            director=new_movie['director'],
            year=new_movie['year'],  # int
            poster_url=new_movie['poster_url'],  # string
            user_id=new_movie['user_id']  # int
        )

        # Add movie to the user's movies list
        data_manager.add_movie(new_movie)
        return redirect(url_for('list_movies', user_id=user_id, success=success))

    # API error
    except requests.exceptions.RequestException as _req_error:
        error = 'There is a problem with the API, try again later!'
        return redirect(url_for('list_movies', user_id=user_id, error=error))

    except KeyError as key_error:
        error = f'There is a problem with the key: {key_error}'
        return redirect(url_for('list_movies', user_id=user_id, error=error))

    except TypeError as type_error:
        error = 'There is a problem with the type of response.'
        return redirect(url_for('list_movies', user_id=user_id, error=error))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Manually updates a movie name"""
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Deletes a movie from user's list"""
    try:
        data_manager.delete_movie(movie_id)
        success = 'Movie deleted!'
        return redirect(url_for('list_movies', user_id=user_id, success=success))

    except AttributeError as _attribute_error:
        error = "There is a problem deleting this movie..id doesn\'t exist!"
        return redirect(url_for('list_movies', user_id=user_id, error=error))


if __name__ == '__main__':
    # Run app_context only the first time
    #with app.app_context():
    #    db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)
