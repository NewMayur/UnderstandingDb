from app import app
from models import db, Icon, User
import os

def add_icons_to_db():
    with app.app_context():
        icon_dir = os.path.join(app.root_path, 'static', 'icons')
        for filename in os.listdir(icon_dir):
            if filename.endswith('.png'):
                existing_icon = Icon.query.filter_by(name=filename).first()
                if existing_icon is None:
                    icon_path = os.path.join('static', 'icons', filename)
                    new_icon = Icon(name=filename, path=icon_path)
                    db.session.add(new_icon)
        db.session.commit()

def add_sample_users():
    with app.app_context():
        sample_users = [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"},
            # Add more sample users here as needed
        ]

        for user_data in sample_users:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user is None:
                new_user = User(name=user_data['name'], email=user_data['email'])
                db.session.add(new_user)

        db.session.commit()