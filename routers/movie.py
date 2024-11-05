from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieServices
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies',tags=["Movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieServices(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}',tags=["Movies"], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movies(id: int = Path(ge=1)) -> Movie:
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieServices(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":"Registro no encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/',tags=["Movies"],response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str=Query(min_length=3, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieServices(db).get_movies_by_category(category) 
    #db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.post('/movies',tags=["Movies"], status_code=201, response_model=dict, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieServices(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_router.put('/movies/{id}',tags=["Movies"], response_model=Movie, dependencies=[Depends(JWTBearer())])
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    existsMovie = MovieServices(db).get_movie(id)
    if not existsMovie:
        return JSONResponse(status_code=404,content={"message":"Registro no encontrado"})
    MovieServices(db).update_movie(movie, id)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@movie_router.delete('/movies/{id}',tags=["Movies"],status_code=204,  dependencies=[Depends(JWTBearer())])
def delete_movie(id: int):
    db = Session()
    movie = MovieServices(db).get_movie(id)
    if not movie:
        return JSONResponse(status_code=404,content={"message":"Registro no encontrado"})
    MovieServices(db).delete_movie(id)