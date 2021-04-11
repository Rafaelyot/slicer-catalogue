import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'wz3DefHxgQTElMvACRAs1KgAUDPHgTqq')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = 'simple'
    MONGODB_SETTINGS = {
        # 'username': os.environ.get('MONGO_USERNAME', 'root'),
        # 'password': os.environ.get('MONGO_PASSWORD', 'root'),
        'host': os.environ.get('MONGO_URL', 'localhost'),
        'port': 27012,
        'db': os.environ.get('MONGO_DB', 'catalogues'),
        # 'authentication_source': 'admin'
        # 'replicaset': 'rs0'
    }


class AuthConfig:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASS = os.getenv("POSTGRES_PASS", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "vsLCM")
    POSTGRES_IP = os.getenv("POSTGRES_IP", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    APP_SECRET = os.getenv("APP_SECRET", "tenantManager")
    APP_PORT = os.getenv("APP_PORT", 5000)
    RABBIT_USER = os.getenv("RABBIT_USER", "admin")
    RABBIT_PASS = os.getenv("RABBIT_PASS", "admin")
    RABBIT_IP = os.getenv("RABBIT_IP", "localhost")
    RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)
    IDP_IP = os.getenv("IDP_IP", "localhost")
    IDP_PORT = os.getenv("IDP_PORT", 5002)
    IDP_ENDPOINT = os.getenv("IDP_ENDPOINT", "/validate")


class ProdConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'prod'


class DevConfig(Config):
    """Development configurations"""
    DEBUG = True
    ENV = 'dev'
