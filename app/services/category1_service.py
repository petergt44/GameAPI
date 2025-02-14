"""
Service layer for Category 1 game providers.
"""

import requests

class Category1Service:
    """Base class for Category 1 game providers."""

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        """Login to the game provider."""
        payload = {"username": self.username, "password": self.password}
        response = self.session.post(f"{self.base_url}/api/login", data=payload)
        return response.json()

    def add_user(self, username, password):
        """Add a new user."""
        payload = {
            "username": username,
            "password": password,
            "password_confirmation": password,
        }
        response = self.session.post(f"{self.base_url}/api/player/playerInsert", data=payload)
        return response.json()

    def recharge_user(self, user_id, amount):
        """Recharge a user's balance."""
        payload = {
            "id": user_id,
            "balance": amount,
        }
        response = self.session.post(f"{self.base_url}/api/player/agentRecharge", data=payload)
        return response.json()

    def redeem_user(self, user_id, amount):
        """Redeem from a user's balance."""
        payload = {
            "id": user_id,
            "balance": amount,
        }
        response = self.session.post(f"{self.base_url}/api/player/agentWithdraw", data=payload)
        return response.json()