"""
Base service class for all game providers.
Handles common functionality like session management, caching, and error handling.
"""

import time
import hashlib
import requests
import logging
from abc import ABC, abstractmethod
from flask import current_app
from flask_caching import Cache
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

logger = logging.getLogger("automater")
cache = Cache()

class BaseGameService(ABC):
    provider_name = 'BaseProvider'

    def __init__(self, provider_name=None):
        if provider_name:
            self.provider_name = provider_name
        self.session = requests.Session()
        self.base_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    @property
    @abstractmethod
    def base_url(self):
        """Base URL for the provider's API."""
        raise NotImplementedError("Subclasses must define a base_url property.")

    @abstractmethod
    def login(self, username, password):
        """Authenticate with the provider."""
        pass

    @abstractmethod
    def add_user(self, username, password):
        """Add a new user."""
        pass

    @abstractmethod
    def recharge(self, username, amount):
        """Recharge a user's balance."""
        pass

    @abstractmethod
    def redeem(self, username, amount):
        """Redeem from a user's balance."""
        pass

    @abstractmethod
    def get_balances(self, username):
        """Get user and agent balances."""
        pass

    def _cache_key(self, suffix):
        """Generate a cache key for the provider."""
        return f"{self.provider_name}_{suffix}"

    def _handle_token_expiration(self):
        """Handle token expiration and refresh."""
        cached_token = cache.get(self._cache_key("token"))
        if cached_token and self._validate_token(cached_token):
            return cached_token
        new_token = self._refresh_token()
        cache.set(self._cache_key("token"), new_token, timeout=3600)
        return new_token

    def _make_request(self, method, endpoint, **kwargs):
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, headers=self.base_headers, **kwargs)
            response.raise_for_status()
            try:
                data = response.json()
                # Log the type for debugging
                import logging
                logging.getLogger("automater").debug(f"Response data type: {type(data)}")
                # Ensure data is a dict
                if not isinstance(data, dict):
                    return {"raw": str(data)}
                return data
            except Exception:
                return {"raw": response.text}
        except requests.RequestException as e:
            import logging
            logging.getLogger("automater").error(f"{self.provider_name} API error: {str(e)}")
            return {"error": str(e)}

    def _encrypt(self, data, timestamp):
        """Encrypt data using AES."""
        key = f"123{timestamp}abc".encode()
        cipher = AES.new(key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(pad(data.encode(), AES.block_size))).decode()
