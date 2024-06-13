from fastapi import FastAPI, Request, Response, status
from sqlalchemy.exc import OperationalError
from database import SessionLocal, engine
from sqlalchemy import text

app = FastAPI()

def check_db_connection():
    try:
        # Attempt to connect to the database
        with engine.connect() as connection:
            # Execute a simple query to check the connection
            connection.execute(text('SELECT 1'))
        # Return True if the connection was successful
        return True
    except OperationalError:
        # Return False if there was an OperationalError (indicating a failed connection)
        return False

@app.get("/healthz")
def health_check(response: Response):
    # Check the database connection
    if not check_db_connection():
        # If the connection check fails, return a 503 Service Unavailable response
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    # If the connection check succeeds, return a 200 OK response
    return Response(status_code=status.HTTP_200_OK)

@app.put("/healthz")
@app.post("/healthz")
@app.delete("/healthz")
@app.patch("/healthz",)
def method_not_allowed():
    # Return a 405 Method Not Allowed response for any HTTP method other than GET
    return Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    # Add a 'Cache-Control: no-cache' header to all responses
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response
