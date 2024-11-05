from models.movie import Movie as ModelMovie
from schemas.movie import Movie
class MovieServices():

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(ModelMovie).all()
        return result

    def get_movie(self, id):
        result = self.db.query(ModelMovie).filter(ModelMovie.id == id).first()
        return result

    def get_movies_by_category(self, category):
        result = self.db.query(ModelMovie).filter(ModelMovie.category == category).all()
        return result

    def create_movie(self, movie: Movie):
        newMovie = ModelMovie(**movie.dict())
        self.db.add(newMovie)
        self.db.commit()
        return True

    def update_movie(self, movie: Movie, id):
        movieRecord = self.db.query(ModelMovie).filter(ModelMovie.id == id ).first()
        movieRecord.title = movie.title
        movieRecord.overview = movie.overview
        movieRecord.year = movie.year
        movieRecord.rating = movie.rating
        movieRecord.category = movie.category
        self.db.commit()
        return True

    def delete_movie(self, id):
        movie = self.db.query(ModelMovie).filter(ModelMovie.id == id ).first()
        self.db.delete(movie)
        self.db.commit()
        return True