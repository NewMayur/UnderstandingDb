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