from dotenv import load_dotenv
from flask import Flask
from data_manager import DataManager
from models import db, Movie
import os

# load secrets from .env
load_dotenv()

# Formatting the API url
API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
API_USER_KEY = os.getenv("API_USER_KEY")
API_URL = f"{API_BASE_URL}?i={API_USER_KEY}&apikey={API_KEY}&"

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
def home():
    """
    Home page. Show a list of
    all registered users and
    a form for adding new users
    """
    users = data_manager.get_users()
    return str(users)


@app.route('/users', methods=['POST'])
def add_user():
    """Adds new user to the database, then redirects back to home"""
    pass


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """Shows user's movies"""
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Adds a new movie to a user’s list of movies.
    It generates a Movie object filled with infos
    fetched by OMDb API
    """
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Manually updates a movie name"""
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Deletes a movie from user's list"""
    pass


if __name__ == '__main__':
    # Run app_context only the first time
    #with app.app_context():
    #    db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)
