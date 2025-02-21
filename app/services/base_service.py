"""
Base service class for all game providers.
Handles common functionality like session management, caching, and error handling.
"""
# app/services/base_service.py
import requests
from flask import current_app
from app import cache
import logging

logger = logging.getLogger("automater")

class BaseGameService:
    """Base class for game provider services."""

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self, provider):
        """Initialize with a provider object."""
        self.provider = provider
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        try:
            self._load_cached_data()
        except Exception as e:
            logger.error(f"Failed to load cached data for {self.provider.name}: {e}")
        self.logger = logger  # Ensure logger is set here

    @property
    def base_url(self):
        """Return the provider's base URL."""
        return self.provider.base_url

    def _load_cached_data(self):
        """Load cached headers and cookies."""
        try:
            cached_headers = cache.get(f"{self.provider.name}_headers")
            if cached_headers:
                self.session.headers.update(cached_headers)
            cached_cookies = cache.get(f"{self.provider.name}_cookies")
            if cached_cookies:
                for k, v in cached_cookies.items():
                    self.session.cookies.set(k, v)
        except Exception as e:
            logger.error(f"Cache load error: {e}")

    def _save_cached_data(self):
        """Save headers and cookies to cache."""
        try:
            cache.set(f"{self.provider.name}_headers", dict(self.session.headers), timeout=None)
            cache.set(f"{self.provider.name}_cookies", requests.utils.dict_from_cookiejar(self.session.cookies), timeout=None)
        except Exception as e:
            logger.error(f"Cache save error: {e}")

    def _make_request(self, method, endpoint, **kwargs):
        """Make a request with retry on authentication failure."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        return response

    def login(self):
        """Abstract login method to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement login method")