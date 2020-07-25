from os import environ


class Config(Object):
    """
    Get keys from OS
    """
    SECRET_KEY = environ.get('SECRET_KEY')