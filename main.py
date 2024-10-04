from fastapi import FastAPI, Body, status, Path, Query, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title="First app whit FastApi"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine )
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

class User(BaseModel):
    email: str
    password: str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@carlosramirezflores.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
 
@app.get('/movies',tags=["Movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}',tags=["Movies"], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movies(id: int = Path(ge=1)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message":"Registro no encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

@app.get('/movies/',tags=["Movies"],response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: str=Query(min_length=3, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result))


@app.post('/login', tags=["Auth"])
def login(user: User):
    if user.email == "admin@carlosramirezflores.com" and user.password =="123" :
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.post('/movies',tags=["Movies"], status_code=status.HTTP_201_CREATED, response_model=dict, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie) -> dict:
    db = Session()
    newMovie= MovieModel(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@app.put('/movies/{id}',tags=["Movies"], response_model=Movie, dependencies=[Depends(JWTBearer())])
def update_movie(id: int, movie: Movie)-> dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@app.delete('/movies/{id}',tags=["Movies"], status_code=204 , dependencies=[Depends(JWTBearer())])
def delete_movie(id: int):
    for item in movies:
        if id == item["id"]:
            movies.remove(item)