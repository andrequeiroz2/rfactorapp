import os
from flask import Flask
from flask_restful import Api
from rfactorapp import database
from rfactorapp.task.route import init_route_task


def create_app():
    app = Flask(__name__)

    environment_configuration = os.environ["CONFIGURATION_SETUP"]
    app.config.from_object(environment_configuration)

    database.init_app(app)
    api = Api(app)
    init_route_task(api)

    return app



if __name__ == '__main__':
    create_app().run()
    
