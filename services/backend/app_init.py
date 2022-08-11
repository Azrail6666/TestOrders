from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from flask_cors import CORS

import os
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://channelserviceadmin:QAZplmCvbn1!@db:5432/channelservice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"autoflush": False})

from backend.dbModels.order import *

db.create_all()
