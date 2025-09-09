"""DataManager connected with the db"""
from models import db, User, Movie

class DataManager():
    """Static methods for CRUD operations"""
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        """Get all users"""
        return User.query.all()


    def get_movies(self, user_id: int):
        """Get all movies for a user"""
        return Movie.query.where(user_id == Movie.user_id).all()


    def add_movie(self, movie: Movie):
        """Adds a movie to the database"""
        try:
            if type(movie) is Movie:
                db.session.add(movie)
                db.session.commit()
            else:
                raise TypeError('Movie must be of type Movie')

        except TypeError as error:
            print(f"There is a problem with this movie: {error}")


    def update_movie(self, movie_id, new_title):
        """Updates movie title"""
        selected_movie = Movie.query.get(movie_id)
        selected_movie.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id):
        """Delete movie from database"""
        selected_movie = Movie.query.get(movie_id)
        selected_movie.delete()
        db.session.commit()
