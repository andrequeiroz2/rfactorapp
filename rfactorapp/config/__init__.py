class BaseConfig(object):
    """
    Base Config
    """
    DEBUG = False
    MONGO_DBNAME = 'rfactor'
    MONGO_URI = "mongodb://localhost:27017/rfactor"
    SECRET_KEY = "challengerRfactor"


class DevelopmentConfig(BaseConfig):
    """
    Development Config
    """
    ENV = "development"
    TESTING = True
    DEBUG = True
    FLASK_ENV = "development"

    MONGODB_SETTINGS = {
        'host': 'mongodb://mongodb/test',
    }

    
class TestingConfig(BaseConfig):
    """
    Test Config
    """
    ENV = "testing"
    DEBUG = True
    TESTING = True
    MONGO_DBNAME = 'rfactor'
    MONGO_URI = "mongodb://localhost:27017/rfactor"