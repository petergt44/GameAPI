"""
Service class for Category 3 game providers (e.g., Fire Kirin).
Handles web page interactions and form submissions.
"""

import time
from bs4 import BeautifulSoup
import re
from .base_service import BaseGameService

class Category3Service(BaseGameService):
    """Service for Category 3 providers."""

    ACTION_URL_PATTERNS = {
        "recharge": r"Module/AccountManager/GrantTreasure\.aspx\?param=[A-Za-z0-9]+",
        "redeem": r"Module/AccountManager/ChangeTreasure\.aspx\?param=[A-Za-z0-9]+",
        "password": r"Module/AccountManager/ResetPassWord\.aspx\?param=[A-Za-z0-9]+",
    }

    def _extract_hidden_fields(self, response):
        """Extract __VIEWSTATE and __EVENTVALIDATION from HTML."""
        soup = BeautifulSoup(response.text, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value'] if soup.find('input', {'name': '__VIEWSTATE'}) else None
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value'] if soup.find('input', {'name': '__EVENTVALIDATION'}) else None
        self.logger.debug(f"Extracted fields - VIEWSTATE: {viewstate}, EVENTVALIDATION: {eventvalidation}")
        return viewstate, eventvalidation

    def _extract_dynamic_url(self, response, action):
        """Extract action-specific URL."""
        pattern = self.ACTION_URL_PATTERNS.get(action)
        match = re.search(pattern, response.text)
        if match:
            return f"{self.base_url}/{match.group(0)}"
        self.logger.error(f"[{self.provider.name}] Failed to extract URL for {action}")
        return None

    def _submit_form(self, url, payload):
        """Submit a form and return the response message."""
        response = self._make_request("POST", url, data=payload)
        if response.ok:
            pattern = r'Alter\("([^"]+)"'
            match = re.search(pattern, response.text)
            return match.group(1) if match else "Failed to parse response message"
        return "Server unreachable"

    def login(self, username, password, max_retries=3, retry_delay=3):
        """Log in by submitting the login form."""
        for attempt in range(max_retries):
            try:
                # Initial GET to fetch login page
                response = self._make_request("GET", "/default.aspx")
                self.logger.debug(f"[{self.provider.name}] Login page response: {response.text[:500]}")  # Log first 500 chars
                viewstate, eventvalidation = self._extract_hidden_fields(response)
                if not viewstate or not eventvalidation:
                    self.logger.error(f"[{self.provider.name}] Missing hidden fields, retrying...")
                    time.sleep(retry_delay)
                    continue
                payload = {
                    "__VIEWSTATE": viewstate,
                    "__EVENTVALIDATION": eventvalidation,
                    "txtLoginName": username,
                    "txtLoginPass": password,
                    "txtVerifyCode": "solved-captcha",  # Replace with actual CAPTCHA logic if needed
                    "btnLogin": "Login in",
                }
                self.logger.info(f"[{self.provider.name}] Sending login payload: {payload}")
                response = self._make_request("POST", "/default.aspx", data=payload)
                self.logger.debug(f"[{self.provider.name}] Login response: {response.text[:500]}")
                if "Welcome" in response.text:
                    self._save_cached_data()
                    self.logger.info(f"[{self.provider.name}] Login successful")
                    return {"message": "Login successful"}
                else:
                    self.logger.warning(f"[{self.provider.name}] Login failed, no 'Welcome' in response")
            except Exception as e:
                self.logger.error(f"[{self.provider.name}] Login error: {e}")
            time.sleep(retry_delay)
        self.logger.error(f"[{self.provider.name}] Max login attempts reached")
        return {"message": "Login failed", "error": "Max attempts reached"}

    def add_user(self, username, password):
        """Add a new user by submitting the form."""
        response = self._make_request("GET", "/Module/AccountManager/CreateAccount.aspx")
        if response.ok:
            viewstate, eventvalidation = self._extract_hidden_fields(response)
            if not viewstate or not eventvalidation:
                return {"message": "Failed to add user", "error": "Missing hidden fields"}
            payload = {
                "__EVENTTARGET": "ctl07",
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": eventvalidation,
                "txtAccount": username,
                "txtLogonPass": password,
                "txtLogonPass2": password,
            }
            message = self._submit_form("/Module/AccountManager/CreateAccount.aspx", payload)
            if message == "Added successfully":
                self.logger.info(f"[{self.provider.name}] User {username} added successfully")
                return {"message": "User created", "username": username}
            return {"message": "Failed to add user", "error": message}
        return {"message": "Failed to add user", "error": "Server unreachable"}

    def recharge(self, username, amount):
        """Recharge a user's account."""
        user_id, game_id = self._search_user(username)
        if not user_id or not game_id:
            return {"message": "User not found", "error": "Search failed"}
        payload = {"tourl": "0", "getpassuid": user_id, "getpassgid": game_id}
        response = self._make_request("POST", "/Module/AccountManager/AccountsList.aspx", data=payload)
        if response.ok:
            recharge_url = self._extract_dynamic_url(response, "recharge")
            if not recharge_url:
                return {"message": "Failed to recharge", "error": "Recharge URL not found"}
            recharge_page = self._make_request("GET", recharge_url.split(self.base_url)[1])
            if recharge_page.ok:
                viewstate, eventvalidation = self._extract_hidden_fields(recharge_page)
                if not viewstate or not eventvalidation:
                    return {"message": "Failed to recharge", "error": "Missing hidden fields"}
                recharge_payload = {
                    "__EVENTTARGET": "Button1",
                    "__VIEWSTATE": viewstate,
                    "__EVENTVALIDATION": eventvalidation,
                    "txtAddGold": amount,
                }
                message = self._submit_form(recharge_url.split(self.base_url)[1], recharge_payload)
                if message == "Confirmed successful":
                    self.logger.info(f"[{self.provider.name}] Recharge successful for {username}")
                    return {"message": "Recharged successfully"}
                return {"message": "Failed to recharge", "error": message}
        return {"message": "Failed to recharge", "error": "Server unreachable"}

    def redeem(self, username, amount):
        """Redeem funds from a user's account."""
        user_id, game_id = self._search_user(username)
        if not user_id or not game_id:
            return {"message": "User not found", "error": "Search failed"}
        payload = {"tourl": "1", "getpassuid": user_id, "getpassgid": game_id}
        response = self._make_request("POST", "/Module/AccountManager/AccountsList.aspx", data=payload)
        if response.ok:
            redeem_url = self._extract_dynamic_url(response, "redeem")
            if not redeem_url:
                return {"message": "Failed to redeem", "error": "Redeem URL not found"}
            redeem_page = self._make_request("GET", redeem_url.split(self.base_url)[1])
            if redeem_page.ok:
                viewstate, eventvalidation = self._extract_hidden_fields(redeem_page)
                if not viewstate or not eventvalidation:
                    return {"message": "Failed to redeem", "error": "Missing hidden fields"}
                redeem_payload = {
                    "__EVENTTARGET": "Button1",
                    "__VIEWSTATE": viewstate,
                    "__EVENTVALIDATION": eventvalidation,
                    "txtAddGold": amount,
                }
                message = self._submit_form(redeem_url.split(self.base_url)[1], redeem_payload)
                if message == "Confirmed successful":
                    self.logger.info(f"[{self.provider.name}] Redeem successful for {username}")
                    return {"message": "Redeemed successfully"}
                return {"message": "Failed to redeem", "error": message}
        return {"message": "Failed to redeem", "error": "Server unreachable"}

    def change_password(self, username, new_password):
        """Change a user's password."""
        user_id, game_id = self._search_user(username)
        if not user_id or not game_id:
            return {"message": "User not found", "error": "Search failed"}
        payload = {"tourl": "2", "getpassuid": user_id, "getpassgid": game_id}
        response = self._make_request("POST", "/Module/AccountManager/AccountsList.aspx", data=payload)
        if response.ok:
            password_url = self._extract_dynamic_url(response, "password")
            if not password_url:
                return {"message": "Failed to change password", "error": "Password URL not found"}
            password_page = self._make_request("GET", password_url.split(self.base_url)[1])
            if password_page.ok:
                viewstate, eventvalidation = self._extract_hidden_fields(password_page)
                if not viewstate or not eventvalidation:
                    return {"message": "Failed to change password", "error": "Missing hidden fields"}
                password_payload = {
                    "__EVENTTARGET": "Button1",
                    "__VIEWSTATE": viewstate,
                    "__EVENTVALIDATION": eventvalidation,
                    "txtConfirmPass": new_password,
                    "txtSureConfirmPass": new_password,
                }
                message = self._submit_form(password_url.split(self.base_url)[1], password_payload)
                if message == "Modified success!":
                    self.logger.info(f"[{self.provider.name}] Password changed for {username}")
                    return {"message": "Password changed successfully"}
                return {"message": "Failed to change password", "error": message}
        return {"message": "Failed to change password", "error": "Server unreachable"}

    def get_balances(self, username):
        """Fetch user balance."""
        user_id, game_id = self._search_user(username)
        if not user_id or not game_id:
            return {"message": "User not found", "error": "Search failed"}
        payload = {"getscoreuserid": user_id}
        response = self._make_request("POST", "/Module/AccountManager/AccountsList.aspx", data=payload)
        if response.ok:
            pattern = r"(\d+\.?\d*)@"
            match = re.search(pattern, response.text)
            if match:
                self.logger.info(f"[{self.provider.name}] Balance fetched for {username}")
                return {"message": "Balance fetched", "balance": match.group(1)}
            return {"message": "Failed to fetch balance", "error": "Balance not found"}
        return {"message": "Failed to fetch balance", "error": "Server unreachable"}

    def get_agent_balance(self):
        """Fetch agent's balance."""
        response = self._make_request("GET", "/Module/AccountManager/AccountsList.aspx")
        if response.ok:
            pattern = r'updateBalance\("Balance:(\d+\.?\d*)"\)'
            match = re.search(pattern, response.text)
            if match:
                self.logger.info(f"[{self.provider.name}] Agent balance fetched")
                return {"message": "Agent balance fetched", "balance": match.group(1)}
            return {"message": "Failed to fetch agent balance", "error": "Balance not found"}
        return {"message": "Failed to fetch agent balance", "error": "Server unreachable"}

    def _search_user(self, username):
        """Search for a user by username."""
        payload = {"__EVENTTARGET": "ctl16", "txtSearch": username}
        response = self._make_request("POST", "/Module/AccountManager/AccountsList.aspx", data=payload)
        if response.ok:
            pattern = r"updateSelect\(\s*'(\d+),(\d+)'\s*\)"
            match = re.search(pattern, response.text)
            if match:
                return match.groups()  # Returns (user_id, game_id)
            return None, None
        self.logger.error(f"[{self.provider.name}] User search failed for {username}")
        return None, None