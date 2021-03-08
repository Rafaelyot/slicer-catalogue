import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'wz3DefHxgQTElMvACRAs1KgAUDPHgTqq')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = 'simple'
    MONGODB_SETTINGS = {
        'username': os.environ.get('MONGO_USERNAME', 'root'),
        'password': os.environ.get('MONGO_PASSWORD', 'root'),
        'host': os.environ.get('MONGO_URL', 'localhost'),
        'port': 27017,
        'db': os.environ.get('MONGO_DB', 'catalogues'),
        'authentication_source': 'admin'
    }


class ProdConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'prod'


class DevConfig(Config):
    """Development configurations"""
    DEBUG = True
    ENV = 'dev'
