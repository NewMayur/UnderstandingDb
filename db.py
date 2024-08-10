from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User  # Import the User model
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from flask import request



db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

# Import the User model before calling db.create_all()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    icon = db.Column()

class Icon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Icon {self.name}>'
    

def add_icons_to_db():
    icon_dir = os.path.join(app.root_path, 'static', 'icons')
    print(icon_dir)
    for filename in os.listdir(icon_dir):
        if filename.endswith('.png'):  # Adjust the condition based on the file types in the directory
            # Check if the icon already exists in the database
            existing_icon = Icon.query.filter_by(name=filename).first()
            if existing_icon is None:
                icon_path = os.path.join('static', 'icons', filename)
                new_icon = Icon(name=filename, path=icon_path)
                db.session.add(new_icon)
    db.session.commit()

from flask import render_template

@app.route('/')
def index():
    icons = Icon.query.all()
    return render_template('index.html', icons=icons)

from flask import jsonify

@app.route('/api/icons')
def get_all_icons():
    icons = Icon.query.all()
    icon_list = [{'id': icon.id, 'name': icon.name, 'path': icon.path} for icon in icons]
    return jsonify(icons=icon_list)
    

with app.app_context():
    db.create_all()  # Create all tables including the User table

    # user1 = User(name='Alice', email='alice@example.com')
    # user2 = User(name='Bob', email='bob@example.com')

    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.commit()

    # new_icon = Icon(name='New Icon', path='https://example.com/icon.png')
    # db.session.add(new_icon)
    # db.session.commit()




from flask import jsonify, send_from_directory
import os

from flask import abort



def save_icon_file(icon_file):
    filename = secure_filename(icon_file.filename)
    icon_path = os.path.join(app.root_path, 'static', 'icons', filename)
    icon_file.save(icon_path)
    return os.path.join('static', 'icons', filename)

@app.route('/static/icons/<int:icon_id>', methods=['GET'])
def get_icon(icon_id):
    icon = Icon.query.get_or_404(icon_id)
    if not icon.path:
        abort(404, description="Icon not found")
    icon_url = icon.path
    return jsonify({"icon": icon_url})

@app.route('/static/icons/<path:filename>')
def serve_icon(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    return send_from_directory(os.path.join(app.root_path, 'static', 'icons'), filename)

if __name__ == "__main__":
    with app.app_context():
        add_icons_to_db()
    app.run()