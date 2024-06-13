from unittest.mock import patch  # Import patch from unittest.mock for mocking
from fastapi.testclient import TestClient  # Import TestClient from fastapi.testclient for testing
from main import check_db_connection, app  # Import check_db_connection function and app from main module
from psycopg2 import OperationalError  # Import OperationalError from psycopg2 for simulating database errors

# Test function to check successful database connection
def test_check_db_connection_success():
    assert check_db_connection() == True  # Assert that check_db_connection returns True for successful connection

# Test function to check failed database connection
def test_check_db_connection_failure():
    with patch('main.OperationalError', side_effect=OperationalError):  # Patch OperationalError to simulate database error
        assert check_db_connection() == False  # Assert that check_db_connection returns False for failed connection

# Test function to check successful health check endpoint
def test_health_check_success():
    with TestClient(app) as client:  # Create a TestClient instance for the app
        response = client.get("/healthz")  # Make a GET request to /healthz
        assert response.status_code == 200  # Assert that the response status code is 200 (OK)

# Test function to check failed health check endpoint
def test_health_check_failure():
    with patch('main.check_db_connection', return_value=False):  # Patch check_db_connection to always return False
        with TestClient(app) as client:  # Create a TestClient instance for the app
            response = client.get("/healthz")  # Make a GET request to /healthz
            assert response.status_code == 503  # Assert that the response status code is 503 (Service Unavailable)

# Test function to check method not allowed for non-GET requests
def test_method_not_allowed():
    with TestClient(app) as client:  # Create a TestClient instance for the app
        response = client.put("/healthz")  # Make a PUT request to /healthz
        assert response.status_code == 405  # Assert that the response status code is 405 (Method Not Allowed)
    
    with TestClient(app) as client:  # Create a TestClient instance for the app
        response = client.post("/healthz")  # Make a POST request to /healthz
        assert response.status_code == 405  # Assert that the response status code is 405 (Method Not Allowed)

    with TestClient(app) as client:  # Create a TestClient instance for the app
        response = client.delete("/healthz")  # Make a DELETE request to /healthz
        assert response.status_code == 405  # Assert that the response status code is 405 (Method Not Allowed)

    with TestClient(app) as client:  # Create a TestClient instance for the app
        response = client.patch("/healthz")  # Make a PATCH request to /healthz
        assert response.status_code == 405  # Assert that the response status code is 405 (Method Not Allowed)