from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    notify_via_email = db.Column(db.Boolean, default=True)
    notify_via_sms = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'
