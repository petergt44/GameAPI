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
    SQLALCHEMY_DATABASE_URI = "postgresql://[username]:[password]@[url]:[port]/[db_name]"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
    # Gamebase provider
    GAMEBASE_URL = "https://river-pay.com"


    # Alternative caching machanism
    CACHE_TYPE = 'SimpleCache'

    # Redis Cache
    REDIS_URL = "redis://localhost:6379/0"
    CACHE_TYPE = "RedisCache"


    CACHE_DEFAULT_TIMEOUT = 300