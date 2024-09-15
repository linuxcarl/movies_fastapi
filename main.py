from fastapi import FastAPI

app = FastAPI()
app.title="First app whit FastApi"
app.version = "0.0.1"

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Viva México",
		"overview": "Puras mamadas mexicanas...",
		"year": "2024",
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
def get_movies_by_category(category: str, year: str):
    movies_find = []
    for item in movies:
        if category.lower().strip() == item["category"].lower() and year.lower().strip() == item["year"].lower():
            movies_find.append(item)
    return movies_find
