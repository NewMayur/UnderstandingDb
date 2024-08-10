from flask import Flask, render_template
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables including the User table
        
        add_icons_to_db()
    app.run()
