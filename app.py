from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from seeder import *

# Import the db and models after defining db
from models import db, Icon

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Set up Flask-Migrate
migrate = Migrate(app, db)

@app.route('/')
def index():
    icons = Icon.query.all()
    return render_template('index.html', icons=icons)

@app.route('/seed/users', methods=['POST'])
def seed_users():
    add_sample_users()
    return jsonify({"message": "Sample users added successfully"}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables including the User table

        add_icons_to_db()
        add_sample_users()
    app.run()
