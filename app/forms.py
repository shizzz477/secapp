import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

def strongpasswordcheck(form,field):
    hascap = re.compile(r'[A-Z]')
    haslower = re.compile(r'[a-z]')
    hasdigit = re.compile(r'[0-9]')
    hassymbol = re.compile(r'[\!\@\#\%\&\*\(\)\?\>\<]')
    if not (len(field.data) > 8 and \
           hascap.search(field.data) is not None and \
           haslower.search(field.data) is not None and \
           hasdigit.search(field.data) is not None and \
           hassymbol.search(field.data) is not None):
        raise ValidationError('Password must be at least 9 characters containing a digit,lower case letter, upper case letter, and a symbol')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),strongpasswordcheck])
    # confpassword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

