from .base_service import BaseGameService
import time

class Category1Service(BaseGameService):
    @property
    def base_url(self):
        return current_app.config['CATEGORY1_BASE_URL']

    def login(self, username, password):
        timestamp = str(int(time.time()))
        payload = {
            "username": self._encrypt(username, timestamp),
            "password": self._encrypt(password, timestamp),
            "auth_code": ""
        }
        response = self._make_request("POST", "/api/user/login", json=payload)
        
        # Ensure response is a dictionary and JSON-serializable
        if not isinstance(response, dict):
            return {"error": "Invalid response from provider"}, 500

        return {
            "message": "Login successful",
            "token": response.get('token', ''),
            "provider": self.provider_name
        }

    def add_user(self, username, password):
        token = self._handle_token_expiration()
        payload = {
            "token": token,
            "account": username,
            "pwd": password
        }
        response = self._make_request("POST", "/api/account/savePlayer", json=payload)
        return {
            "message": "User created",
            "user_id": response.get('user_id'),
            "username": username
        }