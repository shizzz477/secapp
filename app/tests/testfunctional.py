################################################################
#
# Functional testing modules for the web application
# purpose of these tests is to focus on the functional aspects of
# application
#
###################################################################
import unittest

from wtforms import ValidationError
from app.forms import strongpasswordcheck
from collections import namedtuple
from app import securedb, app

class TestApplicationFuctional(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('Marc', 'Qweasd!23456')
        self.assertEqual(response.status_code, 200)

    def testValidLogin(self):
        securedb.adduser("Marc", "Qgu&9ijrf")
        response = self.login('Marc', 'Qweasd!23456')
        self.assertEqual(response.status_code, 200)

    def testInValidLogin(self):
        securedb.adduser("Marc", "Qgu&9ijrf")
        response = self.login('Marc', 'Qweasd')
        self.assertEqual(response.status_code, 200)

    def testPasswordStrengthCheck(self):
        field = namedtuple("field", "form data")
        f = field("form","mypasswordddddddddddd")
        with self.assertRaises(ValidationError):
            strongpasswordcheck(None,f)
        f1 = field("form", "Qgu&9ijrf")
        self.assertIsNone(strongpasswordcheck(None, f1))
        f2 = field("form", "Q!W@E#4q")
        with self.assertRaises(ValidationError):
            strongpasswordcheck(None, f2)

    def testpasswordencryption(self):
        securedb.adduser("Marc","Qgu&9ijrf")
        self.assertNotEqual("Qgu&9ijrf",securedb.getUserPassword("Marc"))

    def tearDown(self):
        securedb.clear()

    def register(self, username, password):
        #  data = RegisterForm(username=username, password=password),
        return self.app.post(
            '/register',
            data=dict(password=password, username=username),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
