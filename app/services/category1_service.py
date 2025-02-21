"""
Service class for Category 1 game providers (e.g., Gameroom).
Handles token-based authentication and operations.
"""

import time
from flask import current_app
from .base_service import BaseGameService

class Category1Service(BaseGameService):
    """Service for Category 1 providers."""

    def login(self, username, password, max_retries=3, retry_delay=3):
        """Log in using provider credentials and cache the token."""
        for attempt in range(max_retries):
            try:
                payload = {"username": username, "password": password}
                response = self._make_request("POST", "/api/login", data=payload)
                if response.ok:
                    data = response.json()
                    if data.get("message") == "Users login succeeded":
                        token = data.get("token")
                        self.session.headers["Authorization"] = f"Bearer {token}"
                        self._save_cached_data()
                        self.logger.info(f"[{self.provider.name}] Login successful")
                        return {"message": "Login successful", "token": token}
                else:
                    self.logger.warning(f"[{self.provider.name}] Login failed: {response.text}")
            except Exception as e:
                self.logger.error(f"[{self.provider.name}] Login error: {e}")
            time.sleep(retry_delay)
        self.logger.error(f"[{self.provider.name}] Max login attempts reached")
        return {"message": "Login failed", "error": "Max attempts reached"}

    def add_user(self, username, password):
        """Add a new user to the provider."""
        payload = {
            "username": username,
            "password": password,
            "password_confirmation": password,
        }
        response = self._make_request("POST", "/api/player/playerInsert", json=payload)
        if response.ok:
            data = response.json()
            if data.get("message") == "Insert successful":
                return {"message": "User created", "user_id": data.get("user_id"), "username": username}
            return {"message": "Failed to add user", "error": data.get("message")}
        return {"message": "Failed to add user", "error": response.text}

    def recharge(self, username, amount):
        """Recharge a user's account."""
        user_id_response = self._search_user(username)
        if not user_id_response["user_id"]:
            return {"message": "User not found", "error": user_id_response["error"]}
        
        user_id = user_id_response["user_id"]
        agent_balance_response = self._get_agent_balance()
        if not agent_balance_response["balance"]:
            return {"message": "Failed to get agent balance", "error": agent_balance_response["error"]}

        payload = {
            "id": user_id,
            "available_balance": agent_balance_response["balance"],
            "opera_type": 0,
            "bonus": 0,
            "balance": amount,
            "remark": "",
        }
        response = self._make_request("POST", "/api/player/agentRecharge", json=payload)
        if response.ok:
            data = response.json()
            if data.get("message") == "Recharge successful":
                return {"message": "Recharged successfully"}
            return {"message": "Failed to recharge", "error": data.get("message")}
        return {"message": "Failed to recharge", "error": response.text}

    def _search_user(self, username):
        """Search for a user by username."""
        params = {"account": username}
        response = self._make_request("GET", "/api/player/userList", params=params)
        if response.ok:
            data = response.json()
            if data.get("message") == "Query successful" and data["data"]:
                return {"user_id": data["data"][0]["Id"], "error": None}
            return {"user_id": None, "error": "User not found"}
        return {"user_id": None, "error": "Server unreachable"}

    def _get_agent_balance(self):
        """Get the agent's balance."""
        response = self._make_request("POST", "/api/agent/getMoney")
        if response.ok:
            data = response.json()
            if data.get("message") == "Query successful":
                return {"balance": data["data"], "error": None}
            return {"balance": None, "error": data.get("message")}
        return {"balance": None, "error": "Server unreachable"}