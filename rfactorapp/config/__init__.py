class BaseConfig(object):
    """
    Base Config
    """
    DEBUG = False
    MONGO_DBNAME = 'rfactor'
    MONGO_URI = "mongodb://localhost:27017/rfactor"


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