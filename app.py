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
from seeder import seed

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()  # Create all tables including the User table
        # seed(app)
    app.run()
