# ---------------------------------
# app
# @author: Shi Junjie A178915
# Sat 9 June 2024
# ---------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)