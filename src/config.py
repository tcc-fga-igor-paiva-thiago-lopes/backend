import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CORS_ORIGINS = "*"
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    TESTING = True
    SECRET_KEY = "chave_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
