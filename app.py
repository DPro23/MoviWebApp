from flask import Flask
from data_manager import DataManager
from models import db, Movie
import os

# Connected db
DB_PATH = 'data/movies.db'
# Flask app
app = Flask(__name__)
# flask-sqlalchemy configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, DB_PATH)}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link db and the app
db.init_app(app)

# DataManager object
data_manager = DataManager()


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler"""
    return "<div><h1>404</h1><a href='/'>Back home</a></div>", 404


@app.route('/')
def home():
    """Home page"""
    return "Welcome to MoviWeb App!"


if __name__ == '__main__':
    # Run app_context only the first time
    # with app.app_context():
    #    db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)
