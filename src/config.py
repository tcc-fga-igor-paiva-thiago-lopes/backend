import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CORS_ORIGINS = "*"
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace(
        "postgres://", "postgresql://"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    TESTING = True
    JWT_SECRET_KEY = "chave_secreta"
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
