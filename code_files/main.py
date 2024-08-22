import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from database import engine, get_db
from models import Base, User
from schemas import UserCreate, UserUpdate, UserResponse
from auth import get_current_user
import crud

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Setup JSON logging to /var/log/myapp/app.log
logHandler = logging.FileHandler("/var/log/myapp/app.log")
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/v1/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = crud.create_user(db=db, user=user)
        logger.info("User created successfully", extra={"status_code": status.HTTP_201_CREATED, "user_id": created_user.id})
        return created_user
    except HTTPException as e:
        logger.error("Error creating user", extra={"status_code": status.HTTP_400_BAD_REQUEST, "error": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/v1/user/self", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(current_user: User = Depends(get_current_user)):
    logger.info("User retrieved successfully", extra={"status_code": status.HTTP_200_OK, "user_id": current_user.id})
    return current_user

@app.put("/v1/user/self", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        crud.update_user(db, current_user, user_update)
        logger.info("User updated successfully", extra={"status_code": status.HTTP_204_NO_CONTENT, "user_id": current_user.id})
    except HTTPException as e:
        logger.error("Error updating user", extra={"status_code": status.HTTP_400_BAD_REQUEST, "error": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/healthz")
async def health_check(response: Response, request: Request):
    if await request.body():
        logger.warning("Invalid request body", extra={"status_code": status.HTTP_400_BAD_REQUEST, "method": request.method})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This endpoint does not accept any body content."
        )
    if not check_db_connection():
        logger.error("Database connection failed", extra={"status_code": status.HTTP_503_SERVICE_UNAVAILABLE})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    logger.info("Health check passed", extra={"status_code": status.HTTP_200_OK})
    return Response(status_code=status.HTTP_200_OK)

@app.put("/healthz")
@app.post("/healthz")
@app.delete("/healthz")
@app.patch("/healthz")
@app.head("/healthz")
@app.options("/healthz")
def method_not_allowed():
    logger.warning("Method not allowed", extra={"status_code": status.HTTP_405_METHOD_NOT_ALLOWED, "method": "invalid"})
    return Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    logger.info("No-cache header added", extra={"status_code": response.status_code, "path": request.url.path})
    return response

def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text('SELECT 1'))
        return True
    except OperationalError:
        return False