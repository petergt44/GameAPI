"""
Service implementation for Category 3 game providers.
"""

import time, re
from flask import current_app
from app.services.base_service import BaseGameService

class Category3Service(BaseGameService):
    def __init__(self, provider_name="Category3"):
        super().__init__(provider_name)

    @property
    def base_url(self):
        providers = current_app.config.get("CATEGORY3_PROVIDERS", [])
        return providers[0] if providers else ""

    def login(self, username, password):
        # Simulate fetching hidden form fields from the login page
        viewstate = "extracted_viewstate"
        eventvalidation = "extracted_eventvalidation"
        captcha_code = "solved-captcha"
        payload = {
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": eventvalidation,
            "txtLoginName": username,
            "txtLoginPass": password,
            "txtVerifyCode": captcha_code,
            "btnLogin": "Login in"
        }
        response = self._make_request("POST", "/default.aspx", data=payload)
        return {
            "message": "Login successful",
            "token": "dummy-token",
            "provider": self.provider_name
        }

    def add_user(self, username, password):
        # GET the CreateAccount page to extract hidden fields (simulated)
        viewstate = "extracted_viewstate"
        eventvalidation = "extracted_eventvalidation"
        payload = {
            "__EVENTTARGET": "ctl07",
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": eventvalidation,
            "txtAccount": username,
            "txtLogonPass": password,
            "txtLogonPass2": password
        }
        response = self._make_request("POST", "/Module/AccountManager/CreateAccount.aspx", data=payload)
        return {
            "message": "User created",
            "user_id": "dummy-user-id",
            "username": username
        }

    def recharge(self, username, amount):
        # First, simulate obtaining the accounts list
        _ = self._make_request("GET", "/Module/AccountManager/AccountsList.aspx?timestamp=2025/2/20%200:30:47")
        payload = {"txtAddGold": amount}
        response = self._make_request("POST", "/Module/AccountManager/GrantTreasure.aspx", data=payload)
        return {
            "message": "Recharge successful",
            "amount": amount
        }

    def redeem(self, username, amount):
        _ = self._make_request("GET", "/Module/AccountManager/AccountsList.aspx?timestamp=2025/2/20%200:30:47")
        payload = {"txtAddGold": amount}
        response = self._make_request("POST", "/ChangeTreasure.aspx", data=payload)
        return {
            "message": "Redeem successful",
            "amount": amount
        }

    def reset_password(self, username, new_password):
        payload = {
            "username": username,
            "new_password": new_password
        }
        response = self._make_request(
            "POST",
            "/Module/AccountManager/ResetPassWord.aspx?param=6507DC5C59255DD1A5C7545D2385B859B00E7E53F8C9C3F5EDE51E1DD94B250B",
            json=payload
        )
        return {
            "message": "Password reset successful",
            "username": username
        }

    def get_balances(self, username):
        response = self._make_request(
            "GET",
            "/Module/AccountManager/AccountsHistoryPerson.aspx?param=4641718"
        )
        # Assume response is a dict with key "html" containing balance info
        html_content = response.get("html", "") if response else ""
        match = re.search(r"Balance:(\d+\.?\d*)", html_content)
        balance = match.group(1) if match else "0.00"
        return {"balance": balance}
