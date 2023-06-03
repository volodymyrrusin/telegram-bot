from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .views import *
from .models import *

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tg-bot-database.sqlite'

db.init_app(app)

with app.app_context():
    db.create_all()
