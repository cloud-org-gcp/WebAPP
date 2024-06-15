from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from database import engine, get_db
from models import Base, User
from schemas import UserCreate, UserUpdate, UserResponse, Token
from auth import create_access_token, get_current_user, authenticate_user
import crud

# Load environment variables from .env file
load_dotenv()

# Load environment variables with defaults
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Ensure values are loaded correctly
if not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("Environment variables SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES must be set")

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/v1/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/v1/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = crud.create_user(db=db, user=user)
        return created_user
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/v1/user/self", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@app.put("/v1/user/self", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        crud.update_user(db, current_user, user_update)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/healthz")
async def health_check(response: Response, request: Request):
    if await request.body():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This endpoint does not accept any body content."
        )
    if not check_db_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    return Response(status_code=status.HTTP_200_OK)

@app.put("/healthz")
@app.post("/healthz")
@app.delete("/healthz")
@app.patch("/healthz")
@app.head("/healthz")
@app.options("/healthz")
def method_not_allowed():
    return {"status": "error", "message": "Method not allowed"}, status.HTTP_405_METHOD_NOT_ALLOWED

@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response

def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text('SELECT 1'))
        return True
    except OperationalError:
        return False

