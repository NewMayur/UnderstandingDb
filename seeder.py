from models import db, Icon, Device
import os

def seed(app):
    with app.app_context():
        add_icons_to_db(app)
        add_sample_devices()

def add_icons_to_db(app):
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
    # Add some sample lighting devices
    devices = [
        Device(name="Ceiling Lamp", icon_id=1),
        Device(name="Chandelier", icon_id=2),
        Device(name="Cove Light", icon_id=3),
        Device(name="Desk Lamp", icon_id=4),
        Device(name="Mirror Light", icon_id=5),
        Device(name="Pendant Lights", icon_id=6),
        Device(name="Picture Light", icon_id=7),
        Device(name="Spotlight", icon_id=8),
        Device(name="Step Light", icon_id=9),
        Device(name="Table Lamp", icon_id=10),
        Device(name="Track Light", icon_id=11),
        Device(name="Under Cabinet Light", icon_id=12),
        Device(name="Wall Sconces", icon_id=13)
    ]
    db.session.add_all(devices)
    db.session.commit()