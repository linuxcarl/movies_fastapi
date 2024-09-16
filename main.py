from fastapi import FastAPI, Body, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.title="First app whit FastApi"
app.version = "0.0.1"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str
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

@app.get("/", tags= ["Home"])
def read_root():
    return "hello world get" 

@app.get('/movies',tags=["Movies"])
def get_movies():
    return movies

@app.get('/movies/{id}',tags=["Movies"])
def get_movies(id: int):
    for item in movies:
        if id == item["id"]:
            return item
    return []

@app.get('/movies/',tags=["Movies"])
def get_movies_by_category(category: str, year: int):
    movies_find = []
    for item in movies:
        if category.lower().strip() == item["category"].lower() and year == item["year"]:
            movies_find.append(item)
    return movies_find

@app.post('/movies',tags=["Movies"], status_code=status.HTTP_201_CREATED)
def create_movies(movie: Movie):
    movies.append(movie)
    return movies[-1]

@app.put('/movies/{id}',tags=["Movies"])
def update_movie(id: int, Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = Movie.title
            item["overview"] = Movie.overview
            item["year"] = Movie.year
            item["rating"] = Movie.rating
            item["category"] = Movie.category
            return movies
        
@app.delete('/movies/{id}',tags=["Movies"], status_code=204 )
def delete_movie(id: int):
    for item in movies:
        if id == item["id"]:
            movies.remove(item)