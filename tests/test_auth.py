"""
Unit tests for authentication routes.
"""

import unittest
from app import create_app
from app.models import Account, db

class AuthTestCase(unittest.TestCase):
    """Test case for authentication routes."""

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login(self):
        """Test the login endpoint."""
        response = self.client.post('/admin/api/login', json={
            "username": "admin",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 200)