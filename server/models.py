from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin

from server import app

# Create Database
db = SQLAlchemy(app)
Migrate(app, db)

# Models
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.String(), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)
    notes = db.relationship('Notes', backref='users')
    note_max = db.Column(db.Integer(), default=20, nullable=False)
    profile_picture = db.Column(db.String(), nullable=False)
    thank_you_note = db.Column(db.String(), default="Cảm ơn bạn vì đã gửi lưu bút cho mình ❤️", nullable=False)

class Notes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey('users.id'))
    note_id = db.Column(db.String(), unique=True, nullable=False)
    sender = db.Column(db.String(), nullable=False, default="Anonymous")
    note_content = db.Column(db.Text(), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)