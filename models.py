from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Icon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    path = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Icon {self.name}>'

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    icon_id = db.Column(db.ForeignKey('icon.id'), nullable=False)
    icon = db.relationship('Icon', backref=db.backref('devices', lazy=True))

    def __repr__(self):
        return f'<Device {self.name}>'