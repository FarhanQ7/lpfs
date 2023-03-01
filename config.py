import os

class Config:
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    SECRET_KEY = 'secret_key'

class ProdConfig(Config):
    DEBUG = False

class DevConfig(Config):
    pass

config_by_name = dict(prod=ProdConfig, dev=DevConfig)

def get_config_by_name(name):
    if name in config_by_name:
        return config_by_name[name]
    else:
        return DevConfig

config = get_config_by_name(os.getenv('FLASK_CONFIGURATION', 'dev'))
