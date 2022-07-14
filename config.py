import os

class Config(object):
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/exmyb'
    SQLALCHEMY_ECHO = True