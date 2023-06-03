from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

from .views import *

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tg-bot-database.sqlite'

db.init_app(app)

from .models import *

with app.app_context():
    db.create_all()
