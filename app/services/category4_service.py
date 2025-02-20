"""
Service class for Category 4 game providers (e.g., Vblink).
Handles AES-encrypted payloads and signatures.
"""

import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from .base_service import BaseGameService

class Category4Service(BaseGameService):
    """Service for Category 4 providers."""
    SECRET_KEY = "#s3LEA3RpR6PNmbWtuBCPn!4gS2DNM44"

    def _encrypt_data(self, data, timestamp):
        """Encrypt data using AES."""
        key = f"123{timestamp}abc".encode()
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(encrypted).decode()

    def _finalize_payload(self, data, timestamp):
        """Sign and finalize the payload."""
        data_string = "".join(str(data[k]) for k in sorted(data) if data[k])
        sign = hashlib.md5((data_string + str(timestamp) + self.SECRET_KEY).encode()).hexdigest()
        return {"sign": sign, "stime": timestamp, **data}

    def login(self, max_retries=3, retry_delay=3):
        """Log in using encrypted credentials."""
        for attempt in range(max_retries):
            try:
                timestamp = int(time.time())
                payload = self._finalize_payload({
                    "username": self._encrypt_data(self.provider.username, timestamp),
                    "password": self._encrypt_data(self.provider.password, timestamp),
                    "auth_code": "",
                }, timestamp)
                response = self._make_request("POST", "/api/user/login", json=payload)
                if response.ok:
                    data = response.json()
                    if data.get("code") == 20000:
                        token = data.get("token")
                        self.session.headers["Authorization"] = f"Bearer {token}"
                        self._save_cached_data()
                        self.logger.info(f"[{self.provider.name}] Login successful")
                        return True
            except Exception as e:
                self.logger.error(f"[{self.provider.name}] Login error: {e}")
            time.sleep(retry_delay)
        self.logger.error(f"[{self.provider.name}] Max login attempts reached")
        return False

    def add_user(self, username, password):
        """Add a new user with encrypted payload."""
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self.session.headers.get("Authorization", "").split()[1],
            "account": username,
            "pwd": password,
        }, timestamp)
        response = self._make_request("POST", "/api/account/savePlayer", json=payload)
        if response.ok:
            data = response.json()
            if data.get("code") == 20000:
                return {"message": "User created", "username": username}
            return {"message": "Failed to add user", "error": data.get("message")}
        return {"message": "Failed to add user", "error": response.text}

    def recharge(self, username, amount):
        """Recharge a user's account."""
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self.session.headers.get("Authorization", "").split()[1],
            "account": username,
            "amount": amount,
            "type": 1,
        }, timestamp)
        response = self._make_request("POST", "/api/account/recharge", json=payload)
        if response.ok:
            data = response.json()
            if data.get("code") == 20000:
                return {"message": "Recharged successfully"}
            return {"message": "Failed to recharge", "error": data.get("message")}
        return {"message": "Failed to recharge", "error": response.text}

    def redeem(self, username, amount):
        """Redeem funds from a user's account."""
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self.session.headers.get("Authorization", "").split()[1],
            "account": username,
            "amount": amount,
            "type": 2,
        }, timestamp)
        response = self._make_request("POST", "/api/account/recharge", json=payload)
        if response.ok:
            data = response.json()
            if data.get("code") == 20000:
                return {"message": "Redeemed successfully"}
            return {"message": "Failed to redeem", "error": data.get("message")}
        return {"message": "Failed to redeem", "error": response.text}

    def get_balances(self, username):
        """Fetch user balance."""
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self.session.headers.get("Authorization", "").split()[1],
            "account": username,
        }, timestamp)
        response = self._make_request("POST", "/api/account/balance", json=payload)
        if response.ok:
            data = response.json()
            if data.get("code") == 20000:
                return {"message": "Balance fetched", "balance": data["data"]["balance"]}
            return {"message": "Failed to fetch balance", "error": data.get("message")}
        return {"message": "Failed to fetch balance", "error": response.text}

    def change_password(self, username, new_password):
        """Change a user's password."""
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self.session.headers.get("Authorization", "").split()[1],
            "account": username,
            "new_pwd": new_password,
        }, timestamp)
        response = self._make_request("POST", "/api/account/changePassword", json=payload)
        if response.ok:
            data = response.json()
            if data.get("code") == 20000:
                return {"message": "Password changed successfully"}
            return {"message": "Failed to change password", "error": data.get("message")}
        return {"message": "Failed to change password", "error": response.text}

    def get_agent_balance(self):
        """Fetch agent's balance."""
        timestamp = int(time.time() * 1000)
        payload = self._finalize_payload({
            "token": self.session.headers.get("Authorization", "").split()[1],
        }, timestamp)
        response = self._make_request("POST", "/api/agent/balance", json=payload)
        if response.ok:
            data = response.json()
            if data.get("code") == 20000:
                return {"message": "Agent balance fetched", "balance": data["data"]["balance"]}
            return {"message": "Failed to fetch agent balance", "error": data.get("message")}
        return {"message": "Failed to fetch agent balance", "error": response.text}