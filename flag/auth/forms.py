"""Create form logic."""
from wtforms import Form, StringField, PasswordField, validators, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

class SignupForm(Form):
    """User Signup Form."""
    firstName = StringField('First Name',[validators.Length(min=3, max=50), validators.DataRequired()])                     
    lastName = StringField('Last Name',[validators.Length(min=3, max=50), validators.DataRequired()])
    password = PasswordField('New Password', [ validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    phone = StringField('Phone Number')
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    submit = SubmitField('Register')


class LoginForm(Form):
    """User Login Form."""
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class ForgotForm(Form):
    """Forgot Password Form."""
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    submit = SubmitField('Submit')

class ResetPasswordForm(Form):
    password = PasswordField('New Password', [ validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm New Password')
    submit = SubmitField('Request Password Reset')