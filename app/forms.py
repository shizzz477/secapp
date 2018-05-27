"""
    forms.py

    this module is responsible for defining all the forms as well as
    validation rules for all form fields
"""
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import flask_login

__all__ = [
    'LoginForm',
    'RegisterForm',
    'strongpasswordcheck'
]

def maxlengthvalidation(form,field):
    """ensure attackers cannot use any overflow techniques"""
    if len(field.data) > 20:
        raise ValidationError('Maximum of 20 character are allowed')

def strongpasswordcheck(form,field):
    """enforcing passwords to be at least characters containing a lower case letter, uppercase letter, digit, and symbol"""
    hascap = re.compile(r'[A-Z]')
    haslower = re.compile(r'[a-z]')
    hasdigit = re.compile(r'[0-9]')
    hassymbol = re.compile(r'[\!\@\#\%\&\*\(\)\?]')
    if not (len(field.data) > 8 and \
           hascap.search(field.data) is not None and \
           haslower.search(field.data) is not None and \
           hasdigit.search(field.data) is not None and \
           hassymbol.search(field.data) is not None):
        raise ValidationError("Password must be at least 9 characters containing a digit,lower case letter, upper case letter, and a symbol. Valid symbols (@,#,$,^,?)")

def antiInjection(form,field):
    """if specified for the form field, will not allow users to input potentially malicious strings"""
    xss = re.compile(r"[\'/™€¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾Ņ¿Àā~`()\-+={\}\[\]|;:\"<>,.]")
    sqli =re.compile(r"[&|!~*%]")
    if xss.search(field.data) or sqli.search(field.data):
        raise ValidationError('Invalid XSS/SQLi related characters entered')

class LoginForm(FlaskForm):
    """Form and validation requirements for Login"""
    username = StringField('Username', validators=[DataRequired(),antiInjection,maxlengthvalidation])
    password = PasswordField('Password', validators=[DataRequired(),maxlengthvalidation,antiInjection])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    """Form and validation requirements for RegisterForm"""
    username = StringField('Username', validators=[DataRequired(),antiInjection,maxlengthvalidation])
    password = PasswordField('Password', validators=[DataRequired(),strongpasswordcheck,maxlengthvalidation,antiInjection])
    submit = SubmitField('Register')
