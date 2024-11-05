from fastapi import APIRouter
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import HTMLResponse, JSONResponse

user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

@user_router.post('/login', tags=["Auth"])
def login(user: User):
    if user.email == "admin@mail.com" and user.password =="123" :
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
