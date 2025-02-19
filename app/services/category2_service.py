"""
Service implementation for Category 2 game providers.
"""

import time
from flask import current_app
from app.services.base_service import BaseGameService

class Category2Service(BaseGameService):
    def __init__(self, provider_name="Category2"):
        super().__init__(provider_name)

    @property
    def base_url(self):
        providers = current_app.config.get("CATEGORY2_PROVIDERS", [])
        return providers[0] if providers else ""

    def login(self, username, password):
        payload = {
            "username": username,
            "password": password
        }
        response = self._make_request("POST", "/login", json=payload)
        return {
            "message": "Login successful",
            "token": response.get('token', 'dummy-token') if response else None,
            "provider": self.provider_name
        }

    def add_user(self, new_username, new_password):
        payload = {
            "admin_token": "dummy-admin-token",
            "new_account": new_username,
            "new_password": new_password
        }
        response = self._make_request("POST", "/userManagement/insert", json=payload)
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
        response = self._make_request("POST", "/rechargeRecord", json=payload)
        return {
            "message": "Recharge successful",
            "amount": amount
        }

    def redeem(self, username, amount):
        payload = {
            "username": username,
            "amount": amount
        }
        response = self._make_request("POST", "/redeemRecord", json=payload)
        return {
            "message": "Redeem successful",
            "amount": amount
        }

    def reset_password(self, username, new_password):
        payload = {
            "username": username,
            "new_password": new_password
        }
        response = self._make_request("POST", "/userManagement/resetpassword", json=payload)
        return {
            "message": "Password reset successful",
            "username": username
        }

    def get_balances(self, username):
        payload = {"username": username}
        response = self._make_request("POST", "/api/agent/balance", json=payload)
        return {
            "balance": response.get('balance', '0.00') if response else None
        }