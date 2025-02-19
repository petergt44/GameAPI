"""
Service implementation for Category 4 game providers.
"""

from .base_service import BaseGameService
import hashlib
import time

class Category4Service(BaseGameService):
    SECRET_KEY = "#s3LEA3RpR6PNmbWtuBCPn!4gS2DNM44"

    @property
    def base_url(self):
        return current_app.config['CATEGORY4_BASE_URL']

    def login(self, username, password):
        timestamp = int(time.time())
        payload = self._finalize_payload({
            "username": self._encrypt(username, timestamp),
            "password": self._encrypt(password, timestamp),
            "auth_code": ""
        }, timestamp)
        return self._make_request("POST", "/api/user/login", json=payload)

    def _finalize_payload(self, data, timestamp):
        """Sign and finalize the payload."""
        data_string = "".join(str(data[k]) for k in sorted(data) if data[k])
        sign = hashlib.md5((data_string + str(timestamp) + self.SECRET_KEY).encode("utf-8")).hexdigest()
        return {"sign": sign, "stime": timestamp, **data}

    def add_user(self, username, password):
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self._handle_token_expiration(),
            "account": username,
            "pwd": password
        }, timestamp)
        return self._make_request("POST", "/api/account/savePlayer", json=payload)

    def recharge(self, username, amount):
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self._handle_token_expiration(),
            "account": username,
            "score": amount,
            "user_type": "player"
        }, timestamp)
        return self._make_request("POST", "/api/account/enterScore", json=payload)

    def redeem(self, username, amount):
        return self.recharge(username, -amount)

    def get_balances(self, username):
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self._handle_token_expiration(),
            "account": username,
            "type": 2
        }, timestamp)
        return self._make_request("POST", "/api/search/Account", json=payload)