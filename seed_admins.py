# seed_admins.py
from app import create_app, db
from app.models import Admin
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin = Admin(username='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin account created!")