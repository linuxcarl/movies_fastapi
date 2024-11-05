from models.movie import Movie as ModelMovie
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