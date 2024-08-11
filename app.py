from flask import Flask, render_template, jsonify
from flask_migrate import Migrate

# Import the db and models after defining db
from models import db, Icon, Device

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

def add_sample_devices():
    with app.app_context():
        # Add some sample lighting devices
        device1 = Device(name="Ceiling Lamp", icon_id=1)
        device2 = Device(name="Chandelier", icon_id=2)
        device3 = Device(name="Cove Light", icon_id=3)
        device4 = Device(name="Desk Lamp", icon_id=4)
        device5 = Device(name="Mirror Light", icon_id=5)
        device6 = Device(name="Pendant Lights", icon_id=6)
        device7 = Device(name="Picture Light", icon_id=7)
        device8 = Device(name="Spotlight", icon_id=8)
        device9 = Device(name="Step Light", icon_id=9)
        device10 = Device(name="Table Lamp", icon_id=10)
        device11 = Device(name="Track Light", icon_id=11)
        device12 = Device(name="Under Cabinet Light", icon_id=12)
        device13 = Device(name="Wall Sconces", icon_id=13)

        db.session.add_all([device1, device2, device3, device4, device5, device6,
                            device7, device8, device9, device10, device11, device12, device13])
        db.session.commit()
        

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()  # Create all tables including the User table

        # add_icons_to_db()
        # add_sample_devices()

    app.run()
