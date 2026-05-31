import pytest
import requests_mock
from jsonschema import validate
import json
import os
from utils.api_client import APIClient

BASE_URL = "https://reqres.in"

@pytest.fixture
def client():
    return APIClient(BASE_URL)

@pytest.mark.parametrize("endpoint, method, payload, mock_response, expected_status, schema_type", [
    # --- USERS ENDPOINT ---
    ("/api/users/1", "GET", None, {"id": 1, "name": "George", "job": "Analyst"}, 200, "user"),
    ("/api/users/2", "GET", None, {"id": 2, "name": "Janet", "job": "Engineer"}, 200, "user"),
    ("/api/users/3", "GET", None, {"id": 3, "name": "Emma", "job": "Lead"}, 200, "user"),
    ("/api/users/4", "GET", None, {"id": 4, "name": "Eve", "job": "Dev"}, 200, "user"),
    ("/api/users/999", "GET", None, {}, 404, None),
    ("/api/users", "POST", {"name": "Lekha", "job": "DE"}, {"id": 91, "name": "Lekha", "job": "DE"}, 201, "user"),
    ("/api/users", "POST", {"name": "", "job": ""}, {"id": 92, "name": "", "job": ""}, 201, "user"),
    ("/api/users/1", "PUT", {"name": "Updated"}, {"id": 1, "name": "Updated", "job": "Unchanged"}, 200, "user"),

    # --- PRODUCTS / RESOURCES ENDPOINT ---
    ("/api/unknown", "GET", None, {"id": 1, "name": "cerulean"}, 200, "resource"),
    ("/api/unknown/2", "GET", None, {"id": 2, "name": "fuchsia rose"}, 200, "resource"),
    ("/api/unknown/23", "GET", None, {}, 404, None),

    # --- REGISTER ENDPOINT ---
    ("/api/register", "POST", {"email": "eve.holt@reqres.in", "password": "pistol"}, {"id": 4, "token": "QpwL5tke4Pnpja7X4", "refresh_token": "register_refresh_token_abc123", "expires_in": 3600}, 200, "auth"),
    ("/api/register", "POST", {"email": "sydney@fife"}, {"error": "Missing password"}, 400, None),

    # --- LOGIN ENDPOINT ---
    # --- LOGIN ENDPOINT ---
    ("/api/login", "POST", {"email": "peter@klaven"}, {"error": "Missing password"}, 400, None),
    ("/api/login", "POST", {"password": "cityslicka"}, {"error": "Missing email or username"}, 400, None),

    # --- DELAYED RESPONSE PERFORMANCE ENDPOINT ---
    ("/api/users?delay=3", "GET", None, {"id": 12, "name": "Delayed User", "job": "Tester"}, 200, "user"),
    
    # --- ADDITIONAL SCRIPTS / RESOURCE VERIFICATIONS ---
    ("/api/colors/1", "GET", None, {"id": 1, "color": "red"}, 200, "resource"),
    ("/api/colors/2", "GET", None, {"id": 2, "color": "blue"}, 200, "resource"),
    ("/api/colors/3", "GET", None, {"id": 3, "color": "green"}, 200, "resource"),
    ("/api/colors/99", "GET", None, {}, 404, None)
])
def test_api_endpoint_parametrized_matrix(client, endpoint, method, payload, mock_response, expected_status, schema_type):
    """Executes dynamic structural contracts across variable application sub-domains."""
    
    with requests_mock.Mocker() as mock:
        if method == "GET":
            mock.get(f"{BASE_URL}{endpoint}", json=mock_response, status_code=expected_status)
        elif method == "POST":
            mock.post(f"{BASE_URL}{endpoint}", json=mock_response, status_code=expected_status)
        elif method == "PUT":
            mock.put(f"{BASE_URL}{endpoint}", json=mock_response, status_code=expected_status)

        response = client.request(method, endpoint, json=payload)
        assert response.status_code == expected_status
        
        # Dynamic Contract Schema Matrix Router
        if response.status_code in [200, 201] and schema_type:
            schema_file = f"{schema_type}_schema.json"
            schema_path = os.path.join(os.path.dirname(__file__), "..", "schemas", schema_file)
            
            with open(schema_path) as f:
                target_schema = json.load(f)
                
            validate(instance=response.json(), schema=target_schema)