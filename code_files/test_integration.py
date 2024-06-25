import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from sqlalchemy import create_engine
from database import get_db, Base, engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost/apitest')

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db to use the testing database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    yield client
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_create_user(test_client):
    response = await test_client.post("/v1/user", json={
        "username": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"

@pytest.mark.asyncio
async def test_get_user(test_client):
    response = await test_client.get(
        "/v1/user/self", 
        auth=("test@example.com", "testpassword")
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"

@pytest.mark.asyncio
async def test_update_user(test_client):
    # Update the user's first name, last name, and password
    new_password = "newtestpassword"
    response = await test_client.put(
        "/v1/user/self",
        json={
            "first_name": "UpdatedTest",
            "last_name": "UpdatedUser",
            "password": new_password
        },
        auth=("test@example.com", "testpassword")
    )
    assert response.status_code == 204

    # Verify the user data update
    response = await test_client.get(
        "/v1/user/self",
        auth=("test@example.com", new_password)
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "UpdatedTest"
    assert data["last_name"] == "UpdatedUser"

    # Verify the old password no longer works
    response = await test_client.get(
        "/v1/user/self",
        auth=("test@example.com", "testpassword")
    )
    assert response.status_code == 401  # Unauthorized