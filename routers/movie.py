from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str= Field(min_length=5, max_length=30 )
    overview: str=Field(min_length=5, max_length=200 )
    year: int = Field(le=2030)
    rating: float = Field(le=10, ge=1)
    category: str =Field(min_length=3, max_length=20)
    
    model_config={
        "json_schema_extra":{
        "examples":[{
            "id": 1,
            "title": "Nombre de la pelicula",
            "overview": "Descripción de la pelicula",
            "year": 2024,
            "rating": 9.8,
            "category": "Acción"
        }]
        }
    }
movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": 2009,
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Viva México",
		"overview": "Puras mamadas mexicanas...",
		"year": 2024,
		"rating": 7.8,
		"category": "Mamada"
	}
]


@movie_router.get('/movies',tags=["Movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}',tags=["Movies"], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movies(id: int = Path(ge=1)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message":"Registro no encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/',tags=["Movies"],response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str=Query(min_length=3, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.post('/movies',tags=["Movies"], status_code=201, response_model=dict, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie) -> dict:
    db = Session()
    newMovie= MovieModel(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_router.put('/movies/{id}',tags=["Movies"], response_model=Movie, dependencies=[Depends(JWTBearer())])
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    movieRecord = db.query(MovieModel).filter(MovieModel.id == id ).first()
    movieRecord.title = movie.title
    movieRecord.overview = movie.overview
    movieRecord.year = movie.year
    movieRecord.rating = movie.rating
    movieRecord.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@movie_router.delete('/movies/{id}',tags=["Movies"],status_code=204,  dependencies=[Depends(JWTBearer())])
def delete_movie(id: int):
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie:
        return JSONResponse(status_code=404,content={"message":"Registro no encontrado"})
    db.delete(movie)
    db.commit()