import os
from flask import Flask
from views.vs_blueprint_catalogue import app as vs_blueprint_api
from settings import ProdConfig
from flask_mongoengine import MongoEngine

APPLICATION_NAME = os.environ.get('APPLICATION_NAME', 'catalogues')

app = Flask(APPLICATION_NAME)

# Configurations settings
app.config.from_object(ProdConfig)

# Register flask's blueprints
app.register_blueprint(vs_blueprint_api)

#  Connect database
db = MongoEngine()
db.init_app(app)

app.run(debug=True)
