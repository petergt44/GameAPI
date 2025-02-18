"""
Service implementation for Category 2 game providers.
"""

from .base_service import BaseGameService
import time

class Category2Service(BaseGameService):
    @property
    def base_url(self):
        return current_app.config['CATEGORY2_BASE_URL']

    def login(self, username, password):
        timestamp = str(int(time.time()))
        payload = {
            "agent_name": username,
            "agent_pwd": password,
            "agent_code": self._solve_captcha(),
            "t": timestamp
        }
        return self._make_request("POST", "/api/agent/agentLogin", json=payload)

    def _solve_captcha(self):
        """Solve CAPTCHA using 2Captcha."""
        captcha_url = f"{self.base_url}/api/agent/captcha?t={int(time.time())}"
        captcha_response = self.session.get(captcha_url)
        captcha_base64 = base64.b64encode(captcha_response.content).decode("utf-8")
        try:
            solver = TwoCaptcha(os.getenv("CAPTCHA_API_KEY"))
            result = solver.normal(captcha_base64)
            return result["code"]
        except Exception as e:
            logger.error(f"[{self.provider_name}] Error solving CAPTCHA: {e}")
            return None

    def add_user(self, username, password):
        payload = {
            "account": username,
            "login_pwd": password,
            "check_pwd": password
        }
        return self._make_request("POST", "/api/user/addUser", json=payload)

    def recharge(self, username, amount):
        user_id, _ = self._get_user_id(username)
        payload = {
            "user_id": user_id,
            "type": 1,
            "amount": amount
        }
        return self._make_request("POST", "/api/user/rechargeRedeem", json=payload)

    def redeem(self, username, amount):
        user_id, _ = self._get_user_id(username)
        payload = {
            "user_id": user_id,
            "type": 2,
            "amount": amount
        }
        return self._make_request("POST", "/api/user/rechargeRedeem", json=payload)

    def get_balances(self, username):
        user_id, _ = self._get_user_id(username)
        user_balance = self._make_request("POST", "/api/user/balance", json={"user_id": user_id})
        agent_balance = self._make_request("POST", "/api/agent/balance", json={"agent_id": self._get_agent_id()})
        return {
            "user_balance": user_balance.get("data", {}).get("t"),
            "agent_balance": agent_balance.get("data", {}).get("t")
        }

    def _get_user_id(self, username):
        payload = {"type": 1, "search": username}
        response = self._make_request("POST", "/api/user/userList", json=payload)
        if response and response.get("msg") == "success":
            user_list = response.get("data", {}).get("list", [])
            if user_list:
                return user_list[0].get("user_id"), "Success"
        return None, "User not found"

    def _get_agent_id(self):
        response = self._make_request("POST", "/api/agent/agentList")
        if response and response.get("msg") == "success":
            agent_list = response.get("data", {}).get("list", [])
            if agent_list:
                return agent_list[0].get("agent_id")
        return None