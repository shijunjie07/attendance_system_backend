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

from .routes import *

device_status = {}
mock_classes = {}
ESP_DEVICES = []

APP_SERVER_PORT = 5001
CHECK_INTERVAL = 600  # seconds
from .device_manager import start_status_check_thread


if __name__ == '__main__':
    from .sql_handler import SQLHandler
    sql_handler = SQLHandler()
    start_status_check_thread(sql_handler, CHECK_INTERVAL)
    app.run(debug=True, host='0.0.0.0', port=APP_SERVER_PORT)