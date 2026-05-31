import requests
import time

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self._cache = {}  # Response Caching Layer
        
        # Authentication Stateful Properties
        self.token = None
        self.refresh_token = None
        self.token_expiry_time = 0 

    def update_session_credentials(self, token, refresh_token, expires_in_seconds):
        """Secures the framework session and maps explicit token lifecycle limits."""
        self.token = token
        self.refresh_token = refresh_token
        self.token_expiry_time = time.time() + expires_in_seconds
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def check_and_refresh_session_token(self):
        """Intercepts outbound pipelines to programmatically rotate expired tokens."""
        if self.token and time.time() >= self.token_expiry_time:
            print("\n[AUTH LIFECYCLE] Token expired! Intercepting request to execute token refresh...")
            
            # Simulated backend programmatic refresh endpoint execution
            # refresh_response = self.session.post(f"{self.base_url}/api/refresh", json={"refresh_token": self.refresh_token})
            
            rotated_token = "new_rotated_access_token_999"
            self.update_session_credentials(rotated_token, self.refresh_token, 3600)
            print("[AUTH LIFECYCLE] Token successfully rotated. New token attached to session headers.")
            return True
        return False

    def request(self, method, endpoint, use_cache=False, **kwargs):
        """Unified wrapper handling endpoint routing, caching, and auth lifecycles."""
        # Check token expiration window prior to dispatching request
        self.check_and_refresh_session_token()

        url = f"{self.base_url}{endpoint}"
        method = method.upper()

        # Performance Optimization: Response Caching Check
        if use_cache and method == "GET" and url in self._cache:
            print(f"\n[CACHE HIT] Returning cached response payload for: {url}")
            return self._cache[url]

        response = self.session.request(method, url, **kwargs)

        if use_cache and method == "GET" and response.status_code == 200:
            print(f"[CACHE MISS] Storing response data in cache for: {url}")
            self._cache[url] = response

        return response