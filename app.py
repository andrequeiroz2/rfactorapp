import os
from flask import Flask
from flask_restful import Api
from rfactorapp import database
from rfactorapp.task.route import init_route_task


def create_app():
    app = Flask(__name__)

    environment_configuration = os.environ["CONFIGURATION_SETUP"]
    app.config.from_object(environment_configuration)
    #app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    #    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

    database.init_app(app)
    api = Api(app)
    init_route_task(api)

    return app



if __name__ == '__main__':
    create_app().run()
    
