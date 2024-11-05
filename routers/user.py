from fastapi import APIRouter
from jwt_manager import create_token
from fastapi.responses import HTMLResponse, JSONResponse
from schemas.user import User

user_router = APIRouter()

@user_router.post('/login', tags=["Auth"])
def login(user: User):
    if user.email == "admin@email.com" and user.password =="123" :
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
