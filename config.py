"""

    config.py
        Configuration module for the web application

"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """ configuration forces development environment run and the key for preventing CSRF """
    FLASK_ENV = "development"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'