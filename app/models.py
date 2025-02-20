"""
Database models for the application.
Includes models for accounts, tokens, and API logs.
"""

from app import db
from flask_login import UserMixin
import enum


class RemoteProvider(enum.Enum):
    """Enum for third-party game providers."""
    VBLINK = "VBLINK"
    CATEGORY1 = "CATEGORY1"
    CATEGORY2 = "CATEGORY2"
    CATEGORY3 = "CATEGORY3"
    CATEGORY4 = "CATEGORY4"

class AccountType(enum.Enum):
    """Enum for account types (admin, store, player)."""
    ADMIN = "ADMIN"
    STORE = "STORE"
    PLAYER = "PLAYER"

class Account(UserMixin, db.Model):
    """Model for user accounts."""
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum(AccountType), nullable=False, default=AccountType.PLAYER)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        """Convert the account object to a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "type": self.type.name,
            "created_at": self.created_at.isoformat(),
        }

class Token(db.Model):
    """Model for API tokens."""
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    usage_count = db.Column(db.Integer, nullable=False, default=0)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        """Convert the token object to a dictionary."""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "token": self.token,
            "valid_until": self.valid_until.isoformat(),
            "usage_count": self.usage_count,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat(),
        }


class APILog(db.Model):
    """Model for logging API requests."""
    __tablename__ = 'api_logs'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    token = db.Column(db.String(300), nullable=True)
    remote_provider = db.Column(db.Enum(RemoteProvider), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(300), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    is_successful = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        """Convert the API log object to a dictionary."""
        return {
            "id": self.id,
            "account_id": self.account_id,
            "token": self.token,
            "remote_provider": self.remote_provider.name,
            "method": self.method,
            "path": self.path,
            "status_code": self.status_code,
            "is_successful": self.is_successful,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }

class Provider(db.Model):
    """Model for game providers."""
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.Enum(RemoteProvider), nullable=False)
    base_url = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        """Convert the provider object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.name,
            "base_url": self.base_url,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
        }