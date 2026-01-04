from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User
from datetime import timedelta
from service import user as user_service
from error import Duplicate, Missing

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = user_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/login")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Create access token for user.

    The following is the example of request body:

    http -v -f post localhost:8000/user/login username=yzb password=123456
    POST /user/login HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Content-Length: 28
    Content-Type: application/x-www-form-urlencoded; charset=utf-8
    Host: localhost:8000
    User-Agent: HTTPie/3.2.4

    username=yzb&password=123456

    INFO:     127.0.0.1:54448 - "POST /user/login HTTP/1.1" 200 OK
    HTTP/1.1 200 OK
    content-length: 162
    content-type: application/json
    date: Sat, 03 Jan 2026 07:27:31 GMT
    server: uvicorn

    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5emIiLCJleHAiOjE3Njc0NTc2NTF9.Ntif0yP_HR-PLwUzDS6M-ijuRcmovCZU9YGWBT5LZF0",
        "token_type": "bearer"
    }
    """
    try:
        user = user_service.auth_user(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = user_service.create_access_token(
            {"sub": user.name}, expires_delta=expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail=exc.args[0],
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/create")
def create_user(user: User):
    try:
        return user_service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.args[0])


@router.get("")
def get_all(current_user: User = Depends(get_current_user)) -> list[User]:
    """
    获取所有用户
    """
    return user_service.get_all()


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前认证用户的信息
    """
    return current_user


@router.get("/protected")
async def read_protected_data(current_user: User = Depends(get_current_user)) -> dict:
    """
    受保护的资源，需要认证才能访问
    """
    return {
        "message": "这是一个受保护的资源",
        "user": current_user.name,
        "data": "敏感信息",
    }
