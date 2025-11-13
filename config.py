"""
Configuration settings for the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for Flask app."""
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    # Example: SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST', '127.0.0.1')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://username:password@127.0.0.1:5432/gameapis"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Caching mechanism
    # Caching configuration with Redis
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    CACHE_REDIS_DB = int(os.getenv('REDIS_DB', 0))
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', f'redis://{os.getenv("REDIS_HOST", "localhost")}:{os.getenv("REDIS_PORT", "6379")}/{os.getenv("REDIS_DB", "0")}')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))  # 5 minutes default

    # TwoCaptcha Settings
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "your-2captcha-api-key-here")

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
