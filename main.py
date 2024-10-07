from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router

app = FastAPI()
app.title="First app whit FastApi"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine )
class User(BaseModel):
    email: str
    password: str

@app.post('/login', tags=["Auth"])
def login(user: User):
    if user.email == "admin@carlosramirezflores.com" and user.password =="123" :
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
