import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # importuojame migracijas

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Migrate(app, db)  # Susiejame app ir db.


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(40), unique=True)  # Papildome duomenų bazės modelį nauju stulpeliu.
    message = db.Column(db.Text, nullable=False)

    # papildykime konstruktorių nauja informacija:
    def __init__(self, name, email, message, phone):
        self.name = name
        self.email = email
        self.message = message
        self.phone = phone

    def __repr__(self):
        return f'{self.name} - {self.email}'


