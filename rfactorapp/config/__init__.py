class BaseConfig(object):
    """
    Base Config
    """
    DEBUG = False
    MONGO_URI = "mongo_uri"
    MONGODB_DB = "challeger"
    MONGODB_HOST = '0.0.0.0'
    MONGODB_PORT = 27017


class DevelopmentConfig(BaseConfig):
    """
    Development Config
    """
    ENV = "development"
    TESTING = True
    DEBUG = True
    FLASK_ENV = "development"
    SECRET_KEY = "challengerRfactor"


class TestingConfig(BaseConfig):
    """
    Test Config
    """
    DEBUG = True