import os
from flask import Flask
from api.views.vs_blueprint import app as vs_blueprint_api
from api.views.vs_descriptor import app as vs_descriptor_api
from api.settings import DevConfig
from flask_mongoengine import MongoEngine
from rabbitmq.messaging import MessageReceiver

APPLICATION_NAME = os.environ.get('APPLICATION_NAME', 'catalogues')


def init_flask():
    app = Flask(APPLICATION_NAME)

    # Configurations settings
    app.config.from_object(DevConfig)

    # Register flask's blueprints
    app.register_blueprint(vs_blueprint_api)
    app.register_blueprint(vs_descriptor_api)

    #  Connect database
    db = MongoEngine()
    db.init_app(app)

    app.run()


def init_rabbit():
    message_receiver = MessageReceiver()
    message_receiver.start()


if __name__ == '__main__':
    init_rabbit()
    init_flask()

