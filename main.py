from fastapi import FastAPI, Body, status, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title="First app whit FastApi"
app.version = "0.0.1"

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

@app.get('/movies',tags=["Movies"], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}',tags=["Movies"], response_model=Movie)
def get_movies(id: int = Path(ge=1)) -> Movie:
    for item in movies:
        if id == item["id"]:
             JSONResponse(content=item)
    return JSONResponse(status_code=404,content=[])

@app.get('/movies/',tags=["Movies"],response_model=List[Movie])
def get_movies_by_category(category: str=Query(min_length=3, max_length=15)) -> List[Movie]:
    movies_find = []
    for item in movies:
        if category.lower().strip() == item["category"].lower():
            movies_find.append(item)
    return  JSONResponse(content=movies_find)

@app.post('/movies',tags=["Movies"], status_code=status.HTTP_201_CREATED, response_model=Movie)
def create_movies(movie: Movie) -> Movie:
    movies.append(movie)
    return JSONResponse(content=movies[-1])

@app.put('/movies/{id}',tags=["Movies"], response_model=Movie)
def update_movie(id: int, Movie)-> Movie:
    for item in movies:
        if item["id"] == id:
            item["title"] = Movie.title
            item["overview"] = Movie.overview
            item["year"] = Movie.year
            item["rating"] = Movie.rating
            item["category"] = Movie.category
            return JSONResponse(content=item)
        
@app.delete('/movies/{id}',tags=["Movies"], status_code=204 )
def delete_movie(id: int):
    for item in movies:
        if id == item["id"]:
            movies.remove(item)