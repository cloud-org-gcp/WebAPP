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
from schemas import UserCreate, UserUpdate, UserResponse
from auth import get_current_user
import crud

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

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

