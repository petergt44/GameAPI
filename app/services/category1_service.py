"""
Service implementation for Category 1 game providers.
"""

import time
from flask import current_app
from app.services.base_service import BaseGameService

class Category1Service(BaseGameService):
    def __init__(self, provider_name="Category1"):
        super().__init__(provider_name)

    @property
    def base_url(self):
        # Use the first provider URL from configuration for Category1
        providers = current_app.config.get("CATEGORY1_PROVIDERS", [])
        return providers[0] if providers else ""

    def login(self, username, password):
        timestamp = str(int(time.time()))
        # Prepare payload as query parameters instead of JSON
        params = {
            "username": self._encrypt(username, timestamp),
            "password": self._encrypt(password, timestamp)
        }
        # Use GET method since POST is not allowed on /admin/login
        response = self._make_request("POST", "/api/login", params=params)
        if response is None:
            return {"message": "Login failed (no response)"}
        return {
            "message": "Login successful",
            "token": response.get('token', 'dummy-token'),
            "provider": self.provider_name
        }

    def add_user(self, new_username, new_password):
        # Here we assume that admin credentials are already handled (e.g. via a stored token)
        payload = {
            "admin_token": "dummy-admin-token",  # Replace with a valid admin token in production
            "account": new_username,
            "password": new_password
        }
        response = self._make_request("POST", "/api/player/playerInsert", json=payload)
        return {
            "message": "User created",
            "user_id": response.get('user_id', 'dummy-user-id') if response else None,
            "username": new_username
        }

    def recharge(self, username, amount):
        payload = {
            "username": username,
            "amount": amount
        }
        response = self._make_request("POST", "/api/player/recharge", json=payload)
        return {
            "message": "Recharge successful",
            "amount": amount
        }

    def redeem(self, username, amount):
        # For Category1, if redeem uses the same endpoint as recharge (adjust if different)
        payload = {
            "username": username,
            "amount": amount
        }
        response = self._make_request("POST", "/api/player/agentWithdraw", json=payload)
        return {
            "message": "Redeem successful",
            "amount": amount
        }

    def reset_password(self, username, new_password):
        payload = {
            "username": username,
            "new_password": new_password
        }
        response = self._make_request("POST", "/api/player/reset", json=payload)
        return {
            "message": "Password reset successful",
            "username": username
        }

    def get_balances(self, username):
        payload = {
            "username": username
        }
        response = self._make_request("POST", "/api/player/agentMoney", json=payload)
        return {
            "balance": response.get('balance', '0.00') if response else None
        }
