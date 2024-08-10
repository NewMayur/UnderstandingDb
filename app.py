from flask import Flask, render_template, jsonify
from flask_migrate import Migrate

# Import the db and models after defining db
from models import db, Icon

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Set up Flask-Migrate
migrate = Migrate(app, db)

from routes import *

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables including the User table

        add_icons_to_db()

    app.run()
