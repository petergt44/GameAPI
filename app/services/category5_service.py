"""
Service class for Category 5 game providers
Handles web page interactions and form submissions.
"""

# app/services/category5_service.py
import time
from twocaptcha import TwoCaptcha
from config import Config
from .category4_service import Category4Service  # Assuming Category4Service is updated without encryption

class Category5Service(Category4Service):
    CAPTCHA_API_KEY = Config.CAPTCHA_API_KEY

    def _solve_cloudflare_captcha(self, response):
        if "Cloudflare" not in response.text:
            return None
        self.logger.info(f"[{self.provider.name}] Encountered Cloudflare CAPTCHA")
        try:
            solver = TwoCaptcha(self.CAPTCHA_API_KEY)
            # Extract site key from Cloudflare page if needed (simplified here)
            site_key = "some_site_key"  # Replace with actual extraction logic if available
            result = solver.hcaptcha(sitekey=site_key, url=self.base_url)
            self.logger.info(f"[{self.provider.name}] Cloudflare CAPTCHA solved: {result['code']}")
            return result['code']
        except Exception as e:
            self.logger.error(f"[{self.provider.name}] CAPTCHA solving failed: {e}")
            return None

    def login(self, username, password, max_retries=3, retry_delay=2):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        self.session.headers.update(headers)
        for attempt in range(max_retries):
            try:
                payload = {
                    "username": username,
                    "password": password,
                    "auth_code": "",
                }
                response = self._make_request("POST", "/api/user/login", json=payload, timeout=20)
                self.logger.debug(f"[{self.provider.name}] Login response: {response.text[:500]}")
                if "Cloudflare" in response.text:
                    captcha_code = self._solve_cloudflare_captcha(response)
                    if captcha_code:
                        payload["auth_code"] = captcha_code
                        response = self._make_request("POST", "/api/user/login", json=payload, timeout=20)
                    else:
                        self.logger.error(f"[{self.provider.name}] Blocked by Cloudflare, retrying...")
                        time.sleep(retry_delay)
                        continue
                if response.ok:
                    data = response.json()
                    if data.get("code") == 20000:
                        token = data.get("token")
                        self.session.headers["Authorization"] = f"Bearer {token}"
                        self._save_cached_data()
                        self.logger.info(f"[{self.provider.name}] Login successful")
                        return {"message": "Login successful", "token": token}
                    self.logger.warning(f"[{self.provider.name}] Login failed: {response.text}")
                else:
                    self.logger.warning(f"[{self.provider.name}] Login failed: {response.text}")
            except Exception as e:
                self.logger.error(f"[{self.provider.name}] Login error: {e}")
            time.sleep(retry_delay)
        self.logger.error(f"[{self.provider.name}] Max login attempts reached")
        return {"message": "Login failed", "error": "Max attempts reached or Cloudflare block"}