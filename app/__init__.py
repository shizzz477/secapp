import bcrypt
from flask import Flask, request
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

class SecureUserDB(object):
    def __init__(self):
        self._dict = {}

    def clear(self):
        self._dict.clear()

    def adduser(self,user,passwd):
        if not self.userexists(user):
            encrypted_passwd = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt(12))
            self._dict.update({user:encrypted_passwd})
        else:
            raise ValueError("User already exists in database")

    def checkpassword(self,user,passwd):
        if not self.userexists(user):
            raise ValueError("Invalid user")
        return bcrypt.checkpw(passwd.encode(), self._dict.get(user))

    def getUserPassword(self,user):
        if self.userexists(user):
            return self._dict.get(user)
        return None

    def userexists(self,user):
        return user in self._dict

    def removeuser(self,user):
        if self.userexists(user):
            deleteduser = self._dict.pop(user)
            return deleteduser
        return None

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

securedb = SecureUserDB()
login = LoginManager(app)

from app import routes, models