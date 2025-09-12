"""DataManager connected with the db"""
from models import db, User, Movie

class DataManager():
    """Static methods for CRUD operations"""
    def create_user(self, name:str):
        """Create a new user"""
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return True

        except Exception as general_error:
            print(f"New user can't be created: {general_error}")
            return []


    def get_users(self):
        """Get all users"""
        try:
            return db.session.query(User).all()

        except Exception as general_error:
            print(f"There is a problem to get users list: {general_error}")
            return []


    def get_movies(self, user_id: int):
        """Get all movies for a user"""
        try:
            return db.session.query(Movie).where(user_id == Movie.user_id).all()

        except Exception as general_error:
            print(f"Problem when get movies for this user: {general_error}")
            return []


    def add_movie(self, movie: Movie):
        """Adds a movie to the database"""
        try:
            if type(movie) is Movie:
                db.session.add(movie)
                db.session.commit()
                return True

            raise TypeError('Movie must be of type Movie')

        except TypeError as error:
            print(f"There is a problem with this movie: {error}")


    def update_movie(self, movie_id: int, new_title: str):
        """Updates movie title"""
        try:
            selected_movie = db.session.query(Movie).get(movie_id)
            selected_movie.name = new_title
            db.session.commit()
            return True

        except Exception as general_error:
            print(f"There is a problem with this movie: {general_error}")
            return False


    def delete_movie(self, movie_id: int):
        """Delete a movie from database"""
        try:
            movie = db.session.query(Movie).get(movie_id)
            db.session.delete(movie)
            db.session.commit()
            return True

        except Exception as general_error:
            print(f"There is a problem with this movie: {general_error}")
            return False
