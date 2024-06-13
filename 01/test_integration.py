import requests  # Import the requests module for making HTTP requests
import pytest  # Import pytest for defining fixtures

@pytest.fixture
def base_url():
    # Fixture to define the base URL of the API
    return "http://localhost:8000"

def test_health_check(base_url):
    # Test function to check the health check endpoint
    response = requests.get(f"{base_url}/healthz")  # Make a GET request to the health check endpoint
    assert response.status_code == 200  # Assert that the response status code is 200 (OK)

def test_health_check_failure(base_url):
    # Test function to check the health check endpoint when the database is not available
    # To simulate a database connection failure, you can stop the database server or use other methods
    response = requests.get(f"{base_url}/healthz")  # Make a GET request to the health check endpoint
    assert response.status_code == 503  # Assert that the response status code is 503 (Service Unavailable)
