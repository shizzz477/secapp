import bcrypt
from flask import Flask
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

class SecureUserDB(object):
    def __init__(self):
        self._dict = {}

    def adduser(self,user,passwd):
        if user not in self._dict:
            encrypted_passwd = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt(12))
            self._dict.update({user:encrypted_passwd})
        else:
            raise ValueError("User already exists in database")

    def checkpassword(self,user,passwd):
        if user not in self._dict:
            raise ValueError("Invalid user")
        return bcrypt.checkpw(passwd.encode(), self._dict.get(user))

securedb = SecureUserDB()
login = LoginManager(app)

from app import routes, models