"""

    __init__.py

    this module manages the app package classes and objects

"""
import bcrypt
from flask import Flask, request
from flask_login import LoginManager
from config import Config

__all__ = [
    'securedb',
    'app',
    'login'
]

app = Flask(__name__)
app.config.from_object(Config)

class SecureUserDB(object):
    """ Class thats responsible for maintaining and encrypting user data """
    def __init__(self):
        self._dict = {}

    def clear(self):
        """ clears the database """
        self._dict.clear()

    def adduser(self,user,passwd):
        """ adds a user """
        if not self.userexists(user):
            encrypted_passwd = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt(12))
            self._dict.update({user:encrypted_passwd})
        else:
            raise ValueError("User already exists in database")

    def checkpassword(self,user,passwd):
        """ checks a plain text password against the stored encrypted password """
        if not self.userexists(user):
            raise ValueError("Invalid user")
        return bcrypt.checkpw(passwd.encode(), self._dict.get(user))

    def getUserPassword(self,user):
        """ retieves the salted password from the DB """
        if self.userexists(user):
            return self._dict.get(user)
        return None

    def userexists(self,user):
        """ checks if user exists in the database """
        return user in self._dict

    def removeuser(self,user):
        """ removes a user from the database """
        if self.userexists(user):
            deleteduser = self._dict.pop(user)
            return deleteduser
        return None

def shutdown_server():
    """ shuts down the web application cleanly """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

securedb = SecureUserDB()
login = LoginManager(app)

from app import routes, models