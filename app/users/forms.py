# Import Form and RecaptchaField (optional)
from flask_wtf import Form
from wtforms import TextField, IntegerField, DateTimeField  # BooleanField
from wtforms.validators import Required, Email


# Define the login form (WTForms)
class RegistrationForm(Form):
    first_name = TextField('First Name')
    last_name = TextField('Last Name'),
    email = TextField('Email Address', [Email(), Required(message='Forgot your email address?')])
    age = IntegerField('Age')
    gender = TextField('Gender'),
    birthday = DateTimeField('Your Birthday', format='%m/%d/%y')
    # password = PasswordField('Password', [
    #     Required(message='Must provide a password. ;-)')])
