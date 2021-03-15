from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

db = MongoEngine()


def init_app(app):
    db.init_app(app)
    app.session_interface = MongoEngineSessionInterface(db)
