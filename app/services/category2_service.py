"""
Service class for Category 2 game providers (e.g., Game Vault).
Handles CAPTCHA solving and token-based authentication.
"""

import random
import time
from twocaptcha import TwoCaptcha
from flask import current_app
from .base_service import BaseGameService

class Category2Service(BaseGameService):
    """Service for Category 2 providers."""

    def __init__(self, provider):
        super().__init__(provider)
        self.agent_id = None

    def _generate_t_value(self):
        """Generate a random 8-digit number for CAPTCHA."""
        return random.randint(10000000, 99999999)

    def solve_captcha(self):
        """Solve CAPTCHA using 2Captcha API."""
        t_value = self._generate_t_value()
        captcha_url = f"{self.base_url}/api/agent/captcha?t={t_value}"
        try:
            solver = TwoCaptcha(current_app.config['CAPTCHA_API_KEY'])
            result = solver.normal(captcha_url)
            return result['code'], t_value
        except Exception as e:
            self.logger.error(f"[{self.provider.name}] CAPTCHA solving failed: {e}")
            return None, t_value

    def login(self, max_retries=3, retry_delay=3):
        """Log in using provider credentials and CAPTCHA."""
        for attempt in range(max_retries):
            try:
                agent_code, t_value = self.solve_captcha()
                if not agent_code:
                    continue
                payload = {
                    "agent_name": self.provider.username,
                    "agent_pwd": self.provider.password,
                    "agent_code": agent_code,
                    "t": t_value,
                }
                response = self._make_request("POST", "/api/agent/agentLogin", data=payload)
                if response.ok:
                    data = response.json()
                    if data.get("msg") == "success":
                        token = data["data"]["token"]
                        self.session.headers["Authorization"] = f"Bearer {token}"
                        self._save_cached_data()
                        self.logger.info(f"[{self.provider.name}] Login successful")
                        return True
            except Exception as e:
                self.logger.error(f"[{self.provider.name}] Login error: {e}")
            time.sleep(retry_delay)
        self.logger.error(f"[{self.provider.name}] Max login attempts reached")
        return False

    def _make_request(self, method, endpoint, **kwargs):
        """Override to handle token expiration."""
        response = super()._make_request(method, endpoint, **kwargs)
        if response.status_code == 200:
            data = response.json()
            if data.get("msg") in ["Please login", "Login has expired, please login again", "invalid login status"]:
                if self.login():
                    response = super()._make_request(method, endpoint, **kwargs)
        return response

    def add_user(self, username, password):
        """Add a new user to the provider."""
        payload = {
            "account": username,
            "login_pwd": password,
            "check_pwd": password,
        }
        response = self._make_request("POST", "/api/user/addUser", json=payload)
        if response.ok:
            data = response.json()
            if data.get("msg") == "success":
                return {"message": "User created", "username": username}
            return {"message": "Failed to add user", "error": data.get("msg")}
        return {"message": "Failed to add user", "error": response.text}

    def recharge(self, username, amount):
        """Recharge a user's account."""
        user_id_response = self._search_user(username)
        if not user_id_response["user_id"]:
            return {"message": "User not found", "error": user_id_response["error"]}
        payload = {"user_id": user_id_response["user_id"], "type": 1, "amount": amount}
        response = self._make_request("POST", "/api/user/rechargeRedeem", json=payload)
        if response.ok:
            data = response.json()
            if data.get("msg") == "success":
                return {"message": "Recharged successfully"}
            return {"message": "Failed to recharge", "error": data.get("msg")}
        return {"message": "Failed to recharge", "error": response.text}

    def redeem(self, username, amount):
        """Redeem funds from a user's account."""
        user_id_response = self._search_user(username)
        if not user_id_response["user_id"]:
            return {"message": "User not found", "error": user_id_response["error"]}
        payload = {"user_id": user_id_response["user_id"], "type": 2, "amount": amount}
        response = self._make_request("POST", "/api/user/rechargeRedeem", json=payload)
        if response.ok:
            data = response.json()
            if data.get("msg") == "success":
                return {"message": "Redeemed successfully"}
            return {"message": "Failed to redeem", "error": data.get("msg")}
        return {"message": "Failed to redeem", "error": response.text}

    def get_balances(self, username):
        """Fetch user balance."""
        user_id_response = self._search_user(username)
        if not user_id_response["user_id"]:
            return {"message": "User not found", "error": user_id_response["error"]}
        payload = {"user_id": user_id_response["user_id"]}
        response = self._make_request("POST", "/api/user/balance", json=payload)
        if response.ok:
            data = response.json()
            if data.get("msg") == "success":
                return {"message": "Balance fetched", "balance": data["data"]["balance"]}
            return {"message": "Failed to fetch balance", "error": data.get("msg")}
        return {"message": "Failed to fetch balance", "error": response.text}

    def change_password(self, username, new_password):
        """Change a user's password."""
        user_id_response = self._search_user(username)
        if not user_id_response["user_id"]:
            return {"message": "User not found", "error": user_id_response["error"]}
        payload = {"user_id": user_id_response["user_id"], "new_pwd": new_password}
        response = self._make_request("POST", "/api/user/changePassword", json=payload)
        if response.ok:
            data = response.json()
            if data.get("msg") == "success":
                return {"message": "Password changed successfully"}
            return {"message": "Failed to change password", "error": data.get("msg")}
        return {"message": "Failed to change password", "error": response.text}

    def get_agent_balance(self):
        """Fetch agent's balance."""
        response = self._make_request("GET", "/api/agent/balance")
        if response.ok:
            data = response.json()
            if data.get("msg") == "success":
                return {"message": "Agent balance fetched", "balance": data["data"]["balance"]}
            return {"message": "Failed to fetch agent balance", "error": data.get("msg")}
        return {"message": "Failed to fetch agent balance", "error": response.text}

    def _search_user(self, username):
        """Search for a user by username."""
        payload = {"type": 1, "search": username}
        response = self._make_request("POST", "/api/user/userList", json=payload)
        if response.ok:
            data = response.json()
            if data.get("msg") == "success" and data["data"]["list"]:
                return {"user_id": data["data"]["list"][0]["user_id"], "error": None}
            return {"user_id": None, "error": "User not found"}
        return {"user_id": None, "error": "Server unreachable"}