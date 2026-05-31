import pytest
import requests_mock
from utils.api_client import APIClient

BASE_URL = "https://reqres.in"

@pytest.fixture
def auth_client():
    client = APIClient(BASE_URL)
    client.update_session_credentials("valid_mock_jwt_token", "valid_refresh_token", 3600)
    return client

def test_end_to_end_crud_lifecycle_chain(auth_client):
    """Validates sequential execution dependencies across a clean CRUD pipeline."""
    users_endpoint = "/api/users"
    
    with requests_mock.Mocker() as mock:
        # ---- CREATE (POST) ----
        mock.post(f"{BASE_URL}{users_endpoint}", json={"id": 77, "name": "Lekha Sri", "job": "Associate Analyst"}, status_code=201)
        create_res = auth_client.request("POST", users_endpoint, json={"name": "Lekha Sri", "job": "Associate Analyst"})
        assert create_res.status_code == 201
        dynamic_id = create_res.json()["id"]
        
        # ---- READ (GET) + CACHING VALIDATION ----
        single_user_url = f"{users_endpoint}/{dynamic_id}"
        mock.get(f"{BASE_URL}{single_user_url}", json={"id": 77, "name": "Lekha Sri", "job": "Associate Analyst"}, status_code=200)
        
        # First call triggers standard request processing (Cache Miss)
        get_res_1 = auth_client.request("GET", single_user_url, use_cache=True)
        assert get_res_1.status_code == 200
        
        # Second call intercepts call locally (Cache Hit)
        get_res_2 = auth_client.request("GET", single_user_url, use_cache=True)
        assert id(get_res_1) == id(get_res_2)  # Compares exact identical object in cache memory
        
        # ---- UPDATE (PUT) ----
        mock.put(f"{BASE_URL}{single_user_url}", json={"id": 77, "name": "Lekha Sri", "job": "Data Engineer"}, status_code=200)
        update_res = auth_client.request("PUT", single_user_url, json={"name": "Lekha Sri", "job": "Data Engineer"})
        assert update_res.status_code == 200
        assert update_res.json()["job"] == "Data Engineer"
        
        # ---- DELETE (DELETE) ----
        mock.delete(f"{BASE_URL}{single_user_url}", status_code=204)
        delete_res = auth_client.request("DELETE", single_user_url)
        assert delete_res.status_code == 204