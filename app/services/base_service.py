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
    """Base class for game provider services."""

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    def __init__(self, provider):
        """Initialize with a provider object."""
        self.provider = provider
        self.base_url = provider.url
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self._load_cached_data()
        self.logger = logger

    def _load_cached_data(self):
        """Load cached headers and cookies."""
        cached_headers = cache.get(f"{self.provider.name}_headers")
        if cached_headers:
            self.session.headers.update(cached_headers)
        cached_cookies = cache.get(f"{self.provider.name}_cookies")
        if cached_cookies:
            for k, v in cached_cookies.items():
                self.session.cookies.set(k, v)

    def _save_cached_data(self):
        """Save headers and cookies to cache."""
        cache.set(f"{self.provider.name}_headers", dict(self.session.headers), timeout=None)
        cache.set(f"{self.provider.name}_cookies", requests.utils.dict_from_cookiejar(self.session.cookies), timeout=None)

    def _make_request(self, method, endpoint, **kwargs):
        """Make a request with retry on authentication failure."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return response

    def login(self):
        """Abstract login method to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement login method")
        
