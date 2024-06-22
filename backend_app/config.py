# ---------------------------------
# config
# @author: Shi Junjie A178915
# Sat 8 June 2024
# ---------------------------------

import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///attendance_system_v0.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
