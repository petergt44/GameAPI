"""
Service class for Category 3 game providers (e.g., Fire Kirin).
Handles web page interactions and form submissions.
"""

import time
from bs4 import BeautifulSoup
from .base_service import BaseGameService

class Category3Service(BaseGameService):
    """Service for Category 3 providers."""

    def _extract_hidden_fields(self, response):
        """Extract __VIEWSTATE and __EVENTVALIDATION from HTML."""
        soup = BeautifulSoup(response.text, 'html.parser')
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        return viewstate, eventvalidation

    def login(self, max_retries=3, retry_delay=3):
        """Log in by submitting the login form."""
        for attempt in range(max_retries):
            try:
                response = self._make_request("GET", "/default.aspx")
                viewstate, eventvalidation = self._extract_hidden_fields(response)
                captcha_code = "solved-captcha"  # Replace with actual CAPTCHA solving logic
                payload = {
                    "__VIEWSTATE": viewstate,
                    "__EVENTVALIDATION": eventvalidation,
                    "txtLoginName": self.provider.username,
                    "txtLoginPass": self.provider.password,
                    "txtVerifyCode": captcha_code,
                    "btnLogin": "Login in",
                }
                response = self._make_request("POST", "/default.aspx", data=payload)
                if "Welcome" in response.text:
                    self._save_cached_data()
                    self.logger.info(f"[{self.provider.name}] Login successful")
                    return True
            except Exception as e:
                self.logger.error(f"[{self.provider.name}] Login error: {e}")
            time.sleep(retry_delay)
        self.logger.error(f"[{self.provider.name}] Max login attempts reached")
        return False

    def add_user(self, username, password):
        """Add a new user by submitting the form."""
        response = self._make_request("GET", "/Module/AccountManager/CreateAccount.aspx")
        if response.ok:
            viewstate, eventvalidation = self._extract_hidden_fields(response)
            payload = {
                "__EVENTTARGET": "ctl07",
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": eventvalidation,
                "txtAccount": username,
                "txtLogonPass": password,
                "txtLogonPass2": password,
            }
            response = self._make_request("POST", "/Module/AccountManager/CreateAccount.aspx", data=payload)
            if "Added successfully" in response.text:
                return {"message": "User created", "username": username}
            return {"message": "Failed to add user", "error": "Form submission failed"}
        return {"message": "Failed to add user", "error": "Server unreachable"}

    def recharge(self, username, amount):
        """Recharge a user's account by submitting the form."""
        response = self._make_request("GET", "/Module/AccountManager/Recharge.aspx")
        if response.ok:
            viewstate, eventvalidation = self._extract_hidden_fields(response)
            payload = {
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": eventvalidation,
                "txtUsername": username,
                "txtAmount": amount,
                "btnRecharge": "Submit",
            }
            response = self._make_request("POST", "/Module/AccountManager/Recharge.aspx", data=payload)
            if "Recharge successful" in response.text:
                return {"message": "Recharged successfully"}
            return {"message": "Failed to recharge", "error": "Form submission failed"}
        return {"message": "Failed to recharge", "error": "Server unreachable"}

    def redeem(self, username, amount):
        """Redeem funds from a user's account."""
        response = self._make_request("GET", "/Module/AccountManager/Redeem.aspx")
        if response.ok:
            viewstate, eventvalidation = self._extract_hidden_fields(response)
            payload = {
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": eventvalidation,
                "txtUsername": username,
                "txtAmount": amount,
                "btnRedeem": "Submit",
            }
            response = self._make_request("POST", "/Module/AccountManager/Redeem.aspx", data=payload)
            if "Redeem successful" in response.text:
                return {"message": "Redeemed successfully"}
            return {"message": "Failed to redeem", "error": "Form submission failed"}
        return {"message": "Failed to redeem", "error": "Server unreachable"}

    def get_balances(self, username):
        """Fetch user balance."""
        response = self._make_request("GET", "/Module/AccountManager/Balance.aspx")
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            balance = soup.find('span', {'id': 'userBalance'}).text
            return {"message": "Balance fetched", "balance": balance}
        return {"message": "Failed to fetch balance", "error": "Server unreachable"}

    def change_password(self, username, new_password):
        """Change a user's password."""
        response = self._make_request("GET", "/Module/AccountManager/ChangePassword.aspx")
        if response.ok:
            viewstate, eventvalidation = self._extract_hidden_fields(response)
            payload = {
                "__VIEWSTATE": viewstate,
                "__EVENTVALIDATION": eventvalidation,
                "txtUsername": username,
                "txtNewPassword": new_password,
                "txtConfirmPassword": new_password,
                "btnSubmit": "Change",
            }
            response = self._make_request("POST", "/Module/AccountManager/ChangePassword.aspx", data=payload)
            if "Password changed" in response.text:
                return {"message": "Password changed successfully"}
            return {"message": "Failed to change password", "error": "Form submission failed"}
        return {"message": "Failed to change password", "error": "Server unreachable"}

    def get_agent_balance(self):
        """Fetch agent's balance."""
        response = self._make_request("GET", "/Module/Agent/Balance.aspx")
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            balance = soup.find('span', {'id': 'agentBalance'}).text
            return {"message": "Agent balance fetched", "balance": balance}
        return {"message": "Failed to fetch agent balance", "error": "Server unreachable"}