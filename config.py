import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('postgres')}:{os.getenv('opensesame')}@{os.getenv('127.0.0.1')}:5432/{os.getenv('gameapi')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
