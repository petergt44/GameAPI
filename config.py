"""
Configuration settings for the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for Flask app."""
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('postgres')}:{os.getenv('opensesame')}@{os.getenv('127.0.0.1')}:5432/{os.getenv('gameapi')}"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://hacker:opensesame@127.0.0.1:5432/gameapis"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Caching mechanism
     # Caching configuration with Redis
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 0

    # TwoCaptcha Settings
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "cdfa431906375d3df98956d07371248a")

   # Provider URLs for each category (list all providers)
    CATEGORY1_PROVIDERS = [
        "https://agentserver.gameroom777.com",
        "http://agentserver.cashmachine777.com:8003",
        "https://agentserver.mrallinone777.com",
        "http://agentserver.mafia77777.com:8003",
        "http://agentserver.cashfrenzy777.com:8003",
        "http://agentserver.slots88888.com:8003"
    ]
    CATEGORY2_PROVIDERS = [
        "https://agent.gamevault999.com",
        "https://agent.lasvegassweeps.com",
        "https://ht.juwa777.com"
    ]
    CATEGORY3_PROVIDERS = [
        "https://firekirin.xyz:8888",
        "https://www.pandamaster.vip",
        "https://milkywayapp.xyz:8781",
        "https://orionstars.vip:8781"
    ]
    CATEGORY4_PROVIDERS = [
        "https://gm.vblink777.club",
        "https://ht.ultrapanda.mobi",
        "https://pko.egame99.club"
    ]
    # Gamebase provider (if needed)
    GAMEBASE_URL = "https://river-pay.com"
