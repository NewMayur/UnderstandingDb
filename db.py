from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User  # Import the User model
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate



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

with app.app_context():
    db.create_all()  # Create all tables including the User table

    # user1 = User(name='Alice', email='alice@example.com')
    # user2 = User(name='Bob', email='bob@example.com')

    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.commit()

    new_icon = Icon(name='New Icon', url='https://example.com/icon.png')
    db.session.add(new_icon)
    db.session.commit()


from flask import jsonify, send_from_directory
import os

from flask import abort

@app.route('/api/icon/<int:icon_id>', methods=['GET'])
def get_icon(icon_id):
    icon = Icon.query.get_or_404(icon_id)
    if not icon.path:
        abort(404, description="Icon not found")
    icon_url = f"/static/icons/{icon.path}"
    return jsonify({"icon": icon_url})

@app.route('/static/icons/<path:filename>')
def serve_icon(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    return send_from_directory(os.path.join(app.root_path, 'static', 'icons'), filename)

if __name__ == "__main__":
    app.run()
